# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from odoo import http, modules, SUPERUSER_ID, tools, _


class OutageCategory(models.Model):
    _name = 'outage.category'
    _description = 'Outage Category'

    name = fields.Char(required=True)


class ProblemCategory(models.Model):
    _name = 'problem.category'
    _description = 'Problem Category'

    name = fields.Char(required=True)
    parent_category_id = fields.Many2one('problem.category', string='Parent')
    type = fields.Selection(
        [('fiber', 'Fiber'), ('other', 'Other'), ('power', 'Power'), ('system', 'System'), ('trm', 'TRM')],
        default='fiber', string='Type')


class Maintenance(models.Model):
    _inherit = 'maintenance.request'

    starting_outage_time = fields.Datetime(string="Starting Outage Time", copy=False)
    starting_time = fields.Datetime(string="Start Time", copy=False)
    end_time = fields.Datetime(string="End Time", copy=False)
    site_code = fields.Char(related='equipment_id.site', string='Site ID')
    maintenance_type = fields.Selection(selection_add=[('emergency', 'Emergency')])
    closing_outage_time = fields.Datetime(string="Restoration Time")
    gov = fields.Many2one('region', string='Gov', related='equipment_id.region_id')
    effected_trxs = fields.Integer(string='Effected Trxs')
    effected_cells = fields.Integer(string='Effected Cells')
    effected_sites = fields.Integer(string='Effected Sites')
    bsc_name = fields.Char(string='BSC Name', related='equipment_id.bsc_name')
    tg_number = fields.Integer(string='TG No', related='equipment_id.tg_number')
    tt_issuer = fields.Char(string='TT Issuer')
    tt_no = fields.Char(string='TT No')
    tt_status = fields.Selection([('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
                                 string='TT Status', default='open')
    alarm_time = fields.Datetime(string='Alarm Time')
    ne_type_id = fields.Many2one(comodel_name="ne.type", string="NE Type", related='equipment_id.ne_type_id')
    ne_impacted_id = fields.Many2one(comodel_name="ne.impacted", string="NE Impacted",
                                     related='equipment_id.ne_impacted_id')
    tt_issuing_time = fields.Datetime(string="TT Issuing Time")
    outage_duration = fields.Float(string="Outage duration", compute="_get_outage_duration", store=True)
    outage_duration_str = fields.Char(string="Outage duration", compute="_get_outage_duration", store=True)
    duration_str = fields.Char(string="duration", compute="_get_duration_str", store=True, copy=False)
    alarm_description = fields.Text(string="Alarm description")
    route_cause = fields.Text(string="Root")
    nmc_comment = fields.Html(string="NMC Comment")
    outage_category_id = fields.Many2one(comodel_name="outage.category", string="Outage Category")
    job_order_ids = fields.One2many(comodel_name="maintenance.job.order", inverse_name="maintenance_id")
    job_order_count = fields.Integer(compute='_compute_job_order_count',
                                     store=True, compute_sudo=True)
    id_permission_time = fields.Float(string='ID Permission Time')
    id_permission_time_str = fields.Char(string='ID Permission Time', default='00:00:00')
    vol_str = fields.Char(string='Vol')
    vol_option = fields.Boolean(copy=False)
    in_vol = fields.Float(string='In-vol')
    in_vol_option = fields.Boolean(copy=False)
    in_vol_str = fields.Char(string='In-vol', default='00:00:00')
    problem_category_id = fields.Many2one('problem.category', string='Problem Category')
    sub_category_id = fields.Many2one('problem.category', string='Sub Category')
    why_it_happened = fields.Char(string='Why it happened')
    site_severity = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id',
                                    string='Site Severity')
    action_taken = fields.Char(string='Action Taken')
    any_sp_used = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Any SP Used', default='yes')
    comment = fields.Char(string='Comment')
    kanban_state = fields.Selection(
        [('normal', 'In Progress'), ('blocked', 'Need To Repaired'), ('done', 'Reviewed')],
        string='Kanban State', required=True, default='normal', tracking=True)
    is_team_leader = fields.Boolean(string="", compute='_cheeck_team_leader')
    maintenance_team_id = fields.Many2one(comodel_name="maintenance.team", required=False, )
    technical_inspection_ids = fields.One2many('technical.inspection', 'maintenance_id', string='Technical Inspections')


    @api.model
    def create(self, values):
        draft_stage = self.env['maintenance.stage'].sudo().search([('name', '=', 'New Request')])
        values['stage_id'] =  draft_stage.id        
        return super(Maintenance, self).create(values)


    @api.onchange('kanban_state')
    def _check_maintenance_state(self):
        for request in self:
            request.timer_start = False
            request.timer_last_stop = False
            if request.kanban_state in ['normal', 'blocked']:
                in_progress_stage = self.env['maintenance.stage'].sudo().search([('name', '=', 'In Progress')])
                draft_stage = self.env['maintenance.stage'].sudo().search([('name', '=', 'New Request')])
                request.stage_id = in_progress_stage.id if request.kanban_state == 'normal' else draft_stage.id
                if request.technical_inspection_ids:
                    technical_inspections = self.env['technical.inspection'].sudo().browse(
                        request.technical_inspection_ids._origin.ids)

                    for technical in technical_inspections:
                        technical.state = 'draft'

    @api.onchange('problem_category_id', 'problem_category_id.type')
    def _check_vol_and_in_vol_option(self):
        for request in self:
            if request.problem_category_id and request.problem_category_id.type in ['fiber', 'other']:
                request.in_vol_option = True
                request.vol_option = False
            else:
                request.vol_option = True
                request.in_vol_option = False

    def _cheeck_team_leader(self):
        for rec in self:
            if rec.maintenance_team_id.team_leader_id.id == self.env.user.id:
                rec.is_team_leader = True
            else:
                rec.is_team_leader = False

    @api.onchange('in_vol_option', 'vol_option', 'outage_duration_str')
    def _check_vol_and_in_vol(self):
        for maintenance in self:
            if maintenance.vol_option and maintenance.in_vol_str != '00:00:00':
                maintenance.in_vol_option = False
            elif maintenance.in_vol_option and maintenance.vol_str != '00:00:00':
                maintenance.vol_option = False
            if maintenance.vol_option and maintenance.vol_option and maintenance.outage_duration_str:
                maintenance.vol_str = maintenance.outage_duration_str if maintenance.outage_duration_str else '00:00:00'
            else:
                maintenance.vol_str = '00:00:00'
            if maintenance.in_vol_option and maintenance.in_vol_option and maintenance.outage_duration_str:
                maintenance.in_vol_str = maintenance.outage_duration_str if maintenance.outage_duration_str else '00:00:00'
                maintenance.vol_option = False
            else:
                maintenance.in_vol_str = '00:00:00'

    @api.onchange('sub_category_id')
    def set_parent_category(self):
        for record in self:
            if record.sub_category_id and record.sub_category_id.parent_category_id:
                record.problem_category_id = record.sub_category_id.parent_category_id.id

    def action_timer_start(self):
        self.ensure_one()
        if self.kanban_state != 'blocked':
            super(Maintenance, self).action_timer_start()
            self.write({'tt_status': 'in_progress', 'starting_outage_time': fields.Datetime.now(),
                        'starting_time': fields.Datetime.now()})
        else:
            self.write({'tt_status': 'in_progress','timer_start': fields.Datetime.now()})

    def action_timer_stop(self):
        self.ensure_one()
        if self.maintenance_type in ['corrective', 'emergency']:
            if not self.route_cause:
                raise ValidationError('Route cause is required before stop')
            if not self.why_it_happened:
                raise ValidationError('Why it happened is required before stop')
            if not self.action_taken:
                raise ValidationError('Action taken is required before stop')
            if not self.any_sp_used:
                raise ValidationError('Any sp used is required before stop')

        maintenance_technical_inspections = False
        if self.checklist_ids and self.checklist_ids.filtered(
                lambda cc: cc.is_mandatory):
            maintenance_technical_inspections = self.env['technical.inspection'].sudo().search(
                [('maintenance_id', '=', self.id)])
        if maintenance_technical_inspections and not any(
                (question.yes_answer or question.no_answer) for question in
                maintenance_technical_inspections.question_line_ids):
            raise ValidationError(_("You must answer at least one question"))

        super(Maintenance, self).action_timer_stop()
        start_time = self.timer_start
        if start_time:  # timer was either running or paused
            self.write({'closing_outage_time': fields.Datetime.now(), 'tt_status': 'closed',
                        'end_time': fields.Datetime.now()})

    @api.depends('job_order_ids')
    def _compute_job_order_count(self):
        for record in self:
            record.job_order_count = len(record.job_order_ids)

    def _get_duration(self, date_start, date_stop):
        if not date_start or not date_stop:
            return 0
        dt = date_stop - date_start
        return dt.seconds % (24 * 3600)

    @api.depends('tt_issuing_time', 'closing_outage_time')
    def _get_outage_duration(self):
        for record in self:
            record.outage_duration = record._get_duration(record.tt_issuing_time, record.closing_outage_time)
            hour = record.outage_duration // 3600
            record.outage_duration %= 3600
            duration_minutes = record.outage_duration // 60
            record.outage_duration %= 60

            hours = str(int(hour)) if hour else '00'
            minutes = str(int(duration_minutes)) if duration_minutes else '00'
            seconds = str(int(record.outage_duration)) if record.outage_duration else '00'
            hours_str = '0' + hours if len(hours) == 1 else hours
            minutes_str = '0' + minutes if len(minutes) == 1 else minutes
            seconds_str = '0' + seconds if len(seconds) == 1 else seconds
            record.outage_duration_str = hours_str + ':' + minutes_str + ':' + seconds_str
            record.in_vol = record.outage_duration

    @api.depends('starting_time', 'end_time')
    def _get_duration_str(self):
        for record in self:
            duration_seconds = record._get_duration(record.starting_time, record.end_time)
            hour = duration_seconds // 3600
            duration_seconds %= 3600
            duration_minutes = duration_seconds // 60
            duration_seconds %= 60
            hours = str(int(hour)) if hour else '00'
            minutes = str(int(duration_minutes)) if duration_minutes else '00'
            seconds = str(int(duration_seconds)) if duration_seconds else '00'
            hours_str = '0' + hours if len(hours) == 1 else hours
            minutes_str = '0' + minutes if len(minutes) == 1 else minutes
            seconds_str = '0' + seconds if len(seconds) == 1 else seconds
            record.duration_str = hours_str + ':' + minutes_str + ':' + seconds_str

    def action_view_job_order(self):
        return {
            'name': _('Job Orders'),
            'res_model': 'maintenance.job.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_maintenance.maintenance_job_order_tree').id, 'tree'),
                (self.env.ref('ejaf_maintenance.maintenance_job_order_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('maintenance_id', '=', self.id)],
        }

    def action_view_checklist(self):
        for record in self:
            ti_obj = self.env['technical.inspection']
            maintenance_inspection = ti_obj.sudo().search([('maintenance_id', '=', record.id)])
            return {
                "type": "ir.actions.act_window",
                "res_model": "technical.inspection",
                "views": [[self.env.ref('ejaf_maintenance.ti_form_view').id, "form"]],
                "res_id": maintenance_inspection[0].id if maintenance_inspection else False,
                'context': {'create': False},
            }


def action_create_job_order(self):
    self.env['maintenance.job.order'].sudo().create({''
                                                     'maintenance_id': self.id,
                                                     'equipment_id': self.equipment_id.id,
                                                     })
    return self.action_view_job_order()

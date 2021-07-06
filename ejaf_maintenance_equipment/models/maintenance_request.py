# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta


class MaintenanceType(models.Model):
    _name = 'maintenance.type'
    _description = 'Maintenance Type'

    name = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive'), ('emergency', 'Emergency')],
                            default='corrective', string='Maintenance Type')


class MaintenanceTag(models.Model):
    _name = 'maintenance.tag'
    _description = 'Maintenance Tag'

    name = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')],
        default='fuel_planning', string='Maintenance Tag')


class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'

    maintenance_type_ids = fields.Many2many('maintenance.type', string='Maintenance Types')
    maintenance_tag_ids = fields.Many2many('maintenance.tag', string='Maintenance Tags')
    show_tags = fields.Boolean(default=False, copy=False)
    team_leader_id = fields.Many2one('res.users', string="Team Leader", domain="[('company_ids', 'in', company_id)]")
    is_manager = fields.Boolean(compute='check_user_is_admin')

    def check_user_is_admin(self):
        self.is_manager = True if self.env.user.has_group('base.group_erp_manager') else False

    @api.onchange('maintenance_type_ids')
    def show_maintenance_tags(self):
        for team in self:
            if team.maintenance_type_ids and team.maintenance_type_ids.filtered(lambda l: l.name == 'preventive'):
                team.show_tags = True
            else:
                team.show_tags = False


class MaintenanceRequestActivity(models.Model):
    _name = 'maintenance.request.activity'
    _description = 'Maintenance Request Activity'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')


class GeneratorRH(models.Model):
    _name = 'generator.rh'

    generator_id = fields.Many2one('site.generator', string='Generator')
    rh = fields.Char(string='RH')
    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request')
    site_id = fields.Many2one('maintenance.equipment', related='maintenance_request_id.equipment_id')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    def _get_default_team(self):
        MT = self.env['maintenance.team']
        corrective_type = self.env['maintenance.type'].sudo().search([('name', '=', 'corrective')], limit=1)
        team = MT.sudo().search(
            [('maintenance_type_ids', 'in', [corrective_type.id]), ('company_id', '=', self.env.company.id)], limit=1)
        if team:
            return team.id
        else:
            return False

    origin = fields.Char(string='Origin')
    maintenance_tag = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')], string='Tag')

    timer_start = fields.Datetime("Timer Start", copy=False)
    timer_first_start = fields.Datetime("Start Date", readonly=True, copy=False)
    timer_last_stop = fields.Datetime("End Date", readonly=True, copy=False)
    starting_time = fields.Datetime(string="Start Time")
    starting_time_date = fields.Date(string="Start Time Date", compute='_calc_dates', store=1)
    end_time = fields.Datetime(string="End Time")
    duration_in_minutes = fields.Float(string='Duration', copy=False)
    timer_first_start_date = fields.Date("Start Date", compute='_calc_dates', store=1)
    checklist_ids = fields.Many2many('check.list', string='Checklists')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team', required=True,
                                          default=_get_default_team, check_company=True)
    planned_generator_ids = fields.Many2many("site.generator", string='Planned Generators')
    pm_status_first_visit = fields.Char(string='PM Status 1st Visit')
    pm_status_first_visit_date = fields.Date(string='Date')
    pm_status_second_visit = fields.Char(string='PM Status 2nd Visit')
    pm_status_second_visit_date = fields.Date(string='Date')
    generator_rh_ids = fields.One2many('generator.rh', 'maintenance_request_id', string='Generator RHs')
    status = fields.Char(string='Status')
    activity = fields.Many2many('maintenance.request.activity', string='Activity')
    remark = fields.Char(string='Remark')

    # fuel fields
    g1rh = fields.Float(string='G1RH')
    g1rh_analysis = fields.Float(string='G1RH', compute='calc_g1_rh')
    g2rh = fields.Float(string='G2RH')
    g2rh_analysis = fields.Float(string='G2RH', compute='calc_g2_rh')
    total_rhs = fields.Float(compute='calc_total_rhs', string='Total RHs')
    days = fields.Float(string='Days', compute='get_days')
    liters_per_hour = fields.Float(string='Liters Per Hour', digits=(16, 2), compute='calc_liters_per_hour')
    tank_size = fields.Float(string='Tank Size', related='equipment_id.tank_size')
    remain_letters = fields.Float(string='Remain Letters in the tank')
    liters_in_the_tank = fields.Float(string='Liters in the tank')
    c_p_status = fields.Char(string='C.P Status')
    filling_liters = fields.Float(string='Filling Liters')
    total_liters = fields.Float(compute='get_total', string='Total Liters')
    rh_per_day = fields.Float(string='R.H/Day', compute='calc_rh_per_day')
    reservation_liters = fields.Float(string='Reservation Liters', related='equipment_id.reservation_liters')
    available_for_use = fields.Float(string='Available for Use', compute='calc_available_for_use')
    remaining_days_before_next_visit = fields.Float(string='Remaining Days before next visit',
                                                    compute='calc_remaining_days_before_next_visit')
    next_visit_plan = fields.Date(string='Next Visit Plan', compute='calc_next_visit_plan',
                                  inverse='_set_next_visit_plan')
    next_visit_plan_temp = fields.Date(string='Next Visit Plan')
    timer_started = fields.Boolean()
    timer_stopped = fields.Boolean()

    @api.depends('g1rh', 'maintenance_type', 'equipment_id', 'maintenance_tag', 'starting_time')
    def calc_g1_rh(self):
        for request in self:
            request.g1rh_analysis = 0
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            if request.g1rh and request.maintenance_type and request.maintenance_type == 'preventive' and request.maintenance_tag and request.maintenance_tag == 'fuel_planning' and request.equipment_id and request.starting_time and request.stage_id.id == repaired_stage.id:
                before_maintenance_req_in_site = self.sudo().search(
                    [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'fuel_planning'),
                     ('stage_id', '=', repaired_stage.id),
                     ('equipment_id', '=', request.equipment_id.id),
                     ('starting_time', '<', request.starting_time)],
                    order="starting_time desc", limit=1)
                request.g1rh_analysis = request.g1rh - before_maintenance_req_in_site.g1rh

    @api.depends('g2rh', 'maintenance_type', 'equipment_id', 'maintenance_tag', 'starting_time')
    def calc_g2_rh(self):
        for request in self:
            request.g2rh_analysis = 0
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            if request.g2rh and request.maintenance_type and request.maintenance_type == 'preventive' and request.maintenance_tag and request.maintenance_tag == 'fuel_planning' and request.equipment_id and request.starting_time and request.stage_id.id == repaired_stage.id:
                before_maintenance_req_in_site = self.sudo().search(
                    [('maintenance_type', '=', 'preventive'), ('equipment_id', '=', request.equipment_id.id),
                     ('maintenance_tag', '=', 'fuel_planning'),
                     ('starting_time', '<', request.starting_time), ('stage_id', '=', repaired_stage.id)],
                    order="starting_time desc", limit=1)
                request.g2rh_analysis = request.g2rh - before_maintenance_req_in_site.g2rh

    
    @api.depends('end_time', 'remaining_days_before_next_visit')
    def calc_next_visit_plan(self):
        for request in self:
            if request.next_visit_plan_temp:
                request.next_visit_plan = request.next_visit_plan_temp
            else:
                repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
                request.next_visit_plan = (request.end_time + timedelta(
                    days=int(
                        request.remaining_days_before_next_visit))) if request.end_time and request.stage_id.id == repaired_stage.id else False

    def _set_next_visit_plan(self):
        for request in self:
            request.next_visit_plan_temp = request.next_visit_plan

    @api.depends('tank_size', 'remain_letters', 'liters_per_hour', 'rh_per_day')
    def calc_remaining_days_before_next_visit(self):
        for req in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            first_part = (
                    req.tank_size / req.remain_letters) if req.remain_letters and req.stage_id.id == repaired_stage.id else 0
            req.remaining_days_before_next_visit = (first_part / (req.liters_per_hour * req.rh_per_day)) if (
                    req.liters_per_hour * req.rh_per_day) else 0

    @api.depends('tank_size', 'reservation_liters')
    def calc_available_for_use(self):
        for record in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            record.available_for_use = (
                    record.tank_size - record.reservation_liters) if record.stage_id.id == repaired_stage.id else 0

    @api.depends('total_rhs', 'days')
    def calc_rh_per_day(self):
        for record in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            record.rh_per_day = (
                    record.total_rhs / record.days) if record.days and record.stage_id.id == repaired_stage.id else 0

    @api.depends('filling_liters', 'total_rhs')
    def calc_liters_per_hour(self):
        for maintenance in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            maintenance.liters_per_hour = (
                    maintenance.filling_liters / maintenance.total_rhs) if maintenance.total_rhs and maintenance.stage_id.id == repaired_stage.id else 0

    @api.depends('g1rh_analysis', 'g2rh_analysis')
    def calc_total_rhs(self):
        for request in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            request.total_rhs = (
                    request.g1rh_analysis + request.g2rh_analysis) if request.stage_id.id == repaired_stage.id else 0

    @api.depends('liters_in_the_tank', 'filling_liters')
    def get_total(self):
        for maintenance in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            maintenance.total_liters = (
                    maintenance.liters_in_the_tank + maintenance.filling_liters) if maintenance.stage_id.id == repaired_stage.id else 0

    @api.depends('equipment_id', 'starting_time')
    def get_days(self):
        for request in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            before_maintenance_req_in_site = self.env['maintenance.request'].sudo().search(
                [('maintenance_type', '=', 'preventive'), ('equipment_id', '=', request.equipment_id.id),
                 ('maintenance_tag', '=', 'fuel_planning'),
                 ('starting_time', '<', request.starting_time), ('stage_id', '=', repaired_stage.id)],
                order="starting_time desc", limit=1)
            diff_days = (
                                request.starting_time - before_maintenance_req_in_site.starting_time).days + 1 if request.starting_time and before_maintenance_req_in_site and before_maintenance_req_in_site.starting_time and request.starting_time >= before_maintenance_req_in_site.starting_time else 0
            request.days = diff_days if request.stage_id.id == repaired_stage.id else False

    @api.onchange('maintenance_tag', 'equipment_id')
    def set_planned_generators(self):
        for request in self:
            if request.equipment_id and request.maintenance_tag == 'generators':
                site_generators = self.env['site.generator'].sudo().search([('site_id', '=', request.equipment_id.id)])
                request.planned_generator_ids = site_generators.ids

    @api.onchange('maintenance_type', 'maintenance_tag')
    @api.depends('maintenance_type', 'maintenance_tag')
    def set_maintenance_team_domain(self):
        for request in self:
            teams = False
            if request.maintenance_type:
                request.maintenance_team_id = False
                maintenance_type_obj = self.env['maintenance.type'].sudo().search(
                    [('name', '=', request.maintenance_type)], limit=1)
                if request.maintenance_type == 'preventive' and request.maintenance_tag:
                    maintenance_tag_obj = self.env['maintenance.tag'].sudo().search(
                        [('name', '=', request.maintenance_tag)], limit=1)
                    teams = self.env['maintenance.team'].sudo().search(
                        [('maintenance_type_ids', 'in', [maintenance_type_obj.id]),
                         ('maintenance_tag_ids', 'in', [maintenance_tag_obj.id])])
                else:
                    teams = self.env['maintenance.team'].sudo().search(
                        [('maintenance_type_ids', 'in', [maintenance_type_obj.id])])
            teams_arr = teams.ids if teams else []
            request.maintenance_team_id = teams[0].id if teams else False
            return {'domain': {
                'maintenance_team_id': [('id', 'in', teams_arr), ('company_id', '=', self.company_id.id)]
            }}

    @api.constrains('checklist_ids')
    def _check_technical_inspection(self):
        for request in self:
            if request.checklist_ids:
                # create questions
                ti_obj = self.env['technical.inspection']
                question_line = self.env['check.list.question.line']
                maintenance_inspection = ti_obj.sudo().search([('maintenance_id', '=', request.id)])
                if not maintenance_inspection:
                    technical_inspection_id = ti_obj.create({
                        'equipment_id': request.equipment_id.id if request.equipment_id else False,
                        'maintenance_id': request.id})
                    for checklist in request.checklist_ids:
                        for question in checklist.check_list_question_ids:
                            question_line.create({
                                'checklist_question_id': question.id,
                                'technical_inspection_id': technical_inspection_id.id,
                            })
                else:
                    checklist_questions = []
                    technical_questions = []
                    technical_inspection_id = maintenance_inspection[0]
                    for checklist in request.checklist_ids:
                        for question in checklist.check_list_question_ids:
                            if question.id not in checklist_questions:
                                checklist_questions.append(question.id)
                            for qq in technical_inspection_id.question_line_ids:
                                if qq.checklist_question_id.id not in technical_questions:
                                    technical_questions.append(qq.checklist_question_id.id)
                        diff = list(set(checklist_questions) - set(technical_questions))
                        for question_id in diff:
                            question_line.create({
                                'checklist_question_id': question_id,
                                'technical_inspection_id': technical_inspection_id.id,
                            })

    @api.onchange('maintenance_tag')
    def set_checklists(self):
        for record in self:
            if record.maintenance_tag:
                checklists = self.env['check.list'].sudo().search(
                    [('type', '=', record.maintenance_tag), ('is_default', '=', True)])
                record.checklist_ids = [(6, 0, checklists.ids)]

    # @api.onchange('maintenance_team_id')
    # def set_responsible(self):
    #     for request in self:
    #         if request.maintenance_team_id and request.maintenance_team_id.team_leader_id:
    #             request.user_id = request.maintenance_team_id.team_leader_id.id
    #             user = request.maintenance_team_id.team_leader_id
    #             partner_ids = [user.partner_id.id]
    #             request.message_notify(
    #                 partner_ids=partner_ids,
    #                 subject=_('Check the maintenance request [%s] for the planning date %s') % (
    #                     request.name, request.request_date),
    #                 message_type='email',
    #                 subtype='mt_comment',
    #             )

    @api.depends('timer_first_start', 'starting_time')
    def _calc_dates(self):
        for rec in self:
            rec.timer_first_start_date = rec.timer_first_start.date() if rec.timer_first_start else False
            rec.starting_time_date = rec.starting_time.date() if rec.starting_time else False

    def action_timer_start(self):
        self.ensure_one()
        self.timer_started = True
        self.timer_stopped = False
        if not self.timer_first_start:
            self.write({'timer_first_start': fields.Datetime.now()})
        stage = self.env['maintenance.stage'].sudo().search([('name', '=', 'In Progress')])
        self.write({'timer_start': fields.Datetime.now(), 'stage_id': stage.id})

    def action_timer_stop(self):
        self.ensure_one()
        self.timer_stopped = True
        start_time = self.timer_start
        if start_time:  # timer was either running or paused
            minutes_spent = round((fields.Datetime.now() - start_time).total_seconds() / 60, 2)
            self.write({'timer_last_stop': fields.Datetime.now(), 'duration_in_minutes': minutes_spent,
                        'duration': minutes_spent * 60 / 3600})
        stage = self.env['maintenance.stage'].sudo().search([('name', '=', 'Repaired')])
        self.write({'stage_id': stage.id})

    def reset_equipment_request(self):
        res = super(MaintenanceRequest, self).reset_equipment_request()
        self.write({
            'timer_started': False,
            'timer_stopped': False,
        })
        return res

    def write(self, vals):
        res = super(MaintenanceRequest, self).write(vals)
        if vals.get('maintenance_team_id', False):
            for request in self:
                if request.maintenance_team_id and request.maintenance_team_id.team_leader_id:
                    request.user_id = request.maintenance_team_id.team_leader_id.id
                    user = request.maintenance_team_id.team_leader_id
                    partner_ids = [user.partner_id.id]
                    request.message_notify(
                        partner_ids=partner_ids,
                        subject=_('Check the maintenance request [%s] for the planning date %s') % (
                            request.name, request.request_date),
                        message_type='email',
                        subtype='mt_comment',
                    )
        return res

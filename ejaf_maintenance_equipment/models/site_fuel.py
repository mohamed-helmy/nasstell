# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class FuelPlanning(models.Model):
    _name = 'fuel.planning'
    _description = 'Fuel Planning'
    _rec_name = 'maintenance_team_id'

    def _get_fuel_teams(self):
        fuel_planning_type = self.env['maintenance.type'].sudo().search([('name', '=', 'preventive')], limit=1)
        fuel_planning_tag = self.env['maintenance.tag'].sudo().search([('name', '=', 'fuel_planning')], limit=1)
        teams = self.env['maintenance.team'].sudo().search(
            [('maintenance_type_ids', 'in', [fuel_planning_type.id]),
             ('maintenance_tag_ids', 'in', [fuel_planning_tag.id])])
        return [('id', 'in', teams.ids)]

    site_id = fields.Many2one(comodel_name="maintenance.equipment", required=False, ondelete="cascade")
    site_name = fields.Char(string='Site Name')
    maintenance_team_id = fields.Many2one(comodel_name="maintenance.team", required=True, domain=_get_fuel_teams)
    planning_lines_ids = fields.One2many(comodel_name="fuel.planning.line", inverse_name="plan_id")

    date_start = fields.Date(string='Start Plan', default=fields.Date.today, required=1)

    @api.onchange('site_id')
    def onchange_site_id(self):
        if self.site_id and self.site_id.maintenance_team_id:
            self.maintenance_team_id = self.site_id.maintenance_team_id
        else:
            self.maintenance_team_id = False
        if self.site_id:
            r = self.env['maintenance.request'].search(
                [('equipment_id', '=', self.site_id.id), ('maintenance_type', '=', 'preventive')],
                order='request_date desc', limit=1)
            if r and r.request_date:
                self.date_start = r.request_date

    @api.model
    def _cron_generate_requests_send_notifications(self):
        subtype_commit = self.env.ref("mail.mt_comment")
        planning_lines = self.env['fuel.planning.line'].search(
            [('date', '>=', fields.Date.today()), ('maintenance_request_id', '=', False)]).filtered(
            lambda x: (x.date - fields.Date.today()).days <= self.env.company.fuel_planning_notify_period)
        for line in planning_lines:
            request = line.create_new_request(line.site_id, line.date, line)
            line.maintenance_request_id = request.id
            # send notification
            if line.maintenance_team_id.team_leader_id:
                user = line.maintenance_team_id.team_leader_id
                partner_ids = [user.partner_id.id]
                request.message_post(
                    partner_ids=partner_ids,
                    subject=_('Check the maintenance request [%s] for the planning date %s') % (
                        request.name, line.date),
                    message_type='email',
                    subtype_id=subtype_commit.id
                )

    def set_actual_dates(self):
        for rec in self:
            for line in rec.planning_lines_ids.filtered(lambda x: x.maintenance_request_id):
                if line.maintenance_request_id.starting_time_date and line.date != line.maintenance_request_id.starting_time_date:
                    line.write({
                        'date_edit_mode': True
                    })

    @api.onchange('date_start','site_id')
    def _fill_lines(self):
        for record in self:
            val = {}
            planning_lines_without_maintenance_requests = self.planning_lines_ids.filtered(
                lambda x: not x.maintenance_request_id)
            self.planning_lines_ids -= planning_lines_without_maintenance_requests
            if record.date_start and record.site_id:
                val['site_id'] = record.site_id.id
                val['date'] = record.date_start
            record.planning_lines_ids = [(0, 0, val)]

    # def action_replan_dates(self):
    #     for rec in self:
    #         rec.set_actual_dates()
    #         lines_with_date_manually_edited = rec.planning_lines_ids.filtered(
    #             lambda x: x.date_edit_mode)
    #         for line_with_date_manually_edited in lines_with_date_manually_edited:
    #             planning_lines_without_maintenance_requests = rec.planning_lines_ids.filtered(
    #                 lambda x: (not x.maintenance_request_id or (
    #                             x.maintenance_request_id and not x.actual_date)) and not x.date_edit_mode and x.id > line_with_date_manually_edited.id)
    #             if planning_lines_without_maintenance_requests and rec.recurring_rule_boundary and rec.recurring_interval:
    #                 last_planned_date = line_with_date_manually_edited.actual_date or line_with_date_manually_edited.date
    #                 for i in range(len(planning_lines_without_maintenance_requests)):
    #                     last_planned_date = rec._get_next_date(rec.recurring_rule_type, rec.recurring_interval,
    #                                                            last_planned_date)
    #                     vals = {
    #                         'date': last_planned_date,
    #                     }
    #                     planning_lines_without_maintenance_requests[i].write(vals)
    #
    #                     # update dates in the maintenance request
    #                     if planning_lines_without_maintenance_requests[i].maintenance_request_id and not \
    #                             planning_lines_without_maintenance_requests[i].actual_date:
    #                         planning_lines_without_maintenance_requests[i].maintenance_request_id.write({
    #                             'request_date': last_planned_date,
    #                             'schedule_date': last_planned_date,
    #                         })
    #
    #             line_with_date_manually_edited.write({
    #                 'date_edit_mode': False
    #             })
    #


class FuelPlanningLine(models.Model):
    _name = 'fuel.planning.line'
    _description = 'Fuel Planning Line'
    _rec_name = 'plan_id'

    site_id = fields.Many2one(comodel_name="maintenance.equipment",related='plan_id.site_id', ondelete="cascade")
    site_name = fields.Char(string='Site Name')
    plan_id = fields.Many2one(comodel_name="fuel.planning", required=True, ondelete="cascade")
    maintenance_request_id = fields.Many2one(comodel_name="maintenance.request")
    maintenance_team_id = fields.Many2one(comodel_name="maintenance.team", related='plan_id.maintenance_team_id',
                                          store=1)
    date = fields.Date(string='Plan For next Visit')
    actual_date = fields.Date(string='Actual Date', related='maintenance_request_id.starting_time_date')
    remain_letters_in_the_tank = fields.Integer(string='Remain Letters In The Tank')
    date_edit_mode = fields.Boolean()


    @api.onchange('date')
    def onchange_date(self):
        self.date_edit_mode = True

    def unlink(self):
        for rec in self:
            if rec.maintenance_request_id:
                raise ValidationError(
                    _('You cannot delete a maintenance planning line which has a maintenance request.'))
        return super(FuelPlanningLine, self).unlink()

    def create_new_request(self, equipment, date, planning_line):
        self.ensure_one()
        return self.env['maintenance.request'].create({
            'name': _('Preventive Fuel Maintenance - %s') % equipment.name,
            'request_date': date,
            'schedule_date': date,
            'maintenance_tag': 'fuel_planning',
            'category_id': equipment.category_id.id,
            'equipment_id': equipment.id,
            'maintenance_type': 'preventive',
            'owner_user_id': equipment.owner_user_id.id,
            'user_id': equipment.technician_user_id.id,
            'maintenance_team_id': planning_line.maintenance_team_id.id,
            'duration': equipment.maintenance_duration,
            'company_id': equipment.company_id.id or self.env.company.id
        })
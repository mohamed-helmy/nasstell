# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SitePlanning(models.Model):
    _name = 'site.planning'
    _rec_name = 'maintenance_team_id'
    _description = 'Site Planning'

    def _get_full_site_teams(self):
        full_site_type = self.env['maintenance.type'].sudo().search([('name', '=', 'preventive')], limit=1)
        full_site_tag = self.env['maintenance.tag'].sudo().search([('name', '=', 'full_site')], limit=1)
        teams = self.env['maintenance.team'].sudo().search(
            [('maintenance_type_ids', 'in', [full_site_type.id]), ('maintenance_tag_ids', 'in', [full_site_tag.id])])
        return [('id', 'in', teams.ids)]

    site_id = fields.Many2one(comodel_name="maintenance.equipment", required=False, ondelete="cascade")
    site_name = fields.Char(string='Site Name')
    maintenance_team_id = fields.Many2one(comodel_name="maintenance.team", required=True, domain=_get_full_site_teams)
    planning_lines_ids = fields.One2many(comodel_name="site.planning.line", inverse_name="plan_id")

    recurring_rule_type = fields.Selection([('daily', 'Days'), ('weekly', 'Weeks'),
                                            ('monthly', 'Months'), ('yearly', 'Years'), ],
                                           string='Recurrence', required=True,
                                           help="repeat at specified interval",
                                           default='monthly', tracking=True)
    recurring_interval = fields.Integer(string="Period", help="Repeat every (Days/Week/Month/Year)",
                                        required=True, default=1, tracking=True)
    recurring_rule_boundary = fields.Selection([
        ('limited', 'Number of repetitions'),
        ('end_date', 'End date'),
    ], string='Recurrence Termination', default='limited', required=1)
    recurring_rule_count = fields.Integer(string="End After", default=1)
    date_start = fields.Date(string='Start Date', default=fields.Date.today, required=1)
    date_end = fields.Date(string='End Date')

    @api.constrains('recurring_rule_count', 'recurring_interval')
    def check_recurring(self):
        for rec in self:
            if rec.recurring_rule_count <= 0:
                raise ValidationError(_('Number of repetitions should be greater than 0.'))
            if rec.recurring_interval <= 0:
                raise ValidationError(_('Period should be greater than 0.'))

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
    def _get_next_date(self, interval_type, interval, current_date):
        recurring_invoice_day = current_date.day
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        interval_type = periods[interval_type]
        recurring_next_date = fields.Date.from_string(current_date) + relativedelta(**{interval_type: interval})
        if interval_type == 'months':
            last_day_of_month = recurring_next_date + relativedelta(day=31)
            if last_day_of_month.day >= recurring_invoice_day:
                # In cases where the next month does not have same day as of previous recurrent date, we set the last date of next month
                # Example: current_date is 31st January then next date will be 28/29th February
                return recurring_next_date.replace(day=recurring_invoice_day)
            # In cases where the date on the last day of a particular month then it should stick to last day for all recurrent months
            # Example: 31st January, 28th February, 31st March, 30 April and so on.
            return last_day_of_month
        # Return the next day after adding interval
        return recurring_next_date

    @api.onchange('date_start', 'date_end', 'recurring_rule_type', 'recurring_rule_count', 'recurring_rule_boundary',
                  'recurring_interval')
    def onchange_date_start(self):
        planning_lines_without_maintenance_requests = self.planning_lines_ids.filtered(
            lambda x: not x.maintenance_request_id)
        self.planning_lines_ids -= planning_lines_without_maintenance_requests
        vals_list = []
        if self.date_start and self.recurring_rule_boundary:
            if self.recurring_rule_boundary == 'limited' and self.recurring_rule_count and self.recurring_interval:
                last_planned_date = self.date_start
                for i in range(self.recurring_rule_count):
                    if i == 0:
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    else:
                        last_planned_date = self._get_next_date(self.recurring_rule_type, self.recurring_interval,
                                                                last_planned_date)
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    vals_list.append((0, 0, vals))
            if self.recurring_rule_boundary == 'end_date' and self.date_end and self.recurring_interval:
                last_planned_date = self.date_start

                i = 0
                while self.date_end > last_planned_date:
                    if i == 0:
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    else:
                        last_planned_date = self._get_next_date(self.recurring_rule_type, self.recurring_interval,
                                                                last_planned_date)
                        last_planned_date = last_planned_date if last_planned_date < self.date_end else self.date_end
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    vals_list.append((0, 0, vals))
                    i += 1

        if vals_list:
            self.planning_lines_ids = vals_list

    def get_week_number(self, date):
        day_weeks = {
            '01': '1',
            '02': '1',
            '03': '1',
            '04': '1',
            '05': '1',
            '06': '1',
            '07': '1',
            '08': '2',
            '09': '2',
            '10': '2',
            '11': '2',
            '12': '2',
            '13': '2',
            '14': '2',
            '15': '3',
            '16': '3',
            '17': '3',
            '18': '3',
            '19': '3',
            '20': '3',
            '21': '3',
            '22': '4',
            '23': '4',
            '24': '4',
            '25': '4',
            '26': '4',
            '27': '4',
            '28': '4',
            '29': '5',
            '30': '5',
            '31': '5',
        }
        day = date.strftime("%d")
        return day_weeks[day]

    def set_actual_dates(self):
        for rec in self:
            for line in rec.planning_lines_ids.filtered(lambda x: x.maintenance_request_id):
                if line.maintenance_request_id.starting_time_date and line.date != line.maintenance_request_id.starting_time_date:
                    line.write({
                        'date_edit_mode': True
                    })

    def action_replan_dates(self):
        for rec in self:
            rec.set_actual_dates()
            lines_with_date_manually_edited = rec.planning_lines_ids.filtered(
                lambda x: x.date_edit_mode)
            for line_with_date_manually_edited in lines_with_date_manually_edited:
                planning_lines_without_maintenance_requests = rec.planning_lines_ids.filtered(
                    lambda x: (not x.maintenance_request_id or (
                            x.maintenance_request_id and not x.actual_date)) and not x.date_edit_mode and x.id > line_with_date_manually_edited.id)
                if planning_lines_without_maintenance_requests and rec.recurring_rule_boundary and rec.recurring_interval:
                    last_planned_date = line_with_date_manually_edited.actual_date or line_with_date_manually_edited.date
                    for i in range(len(planning_lines_without_maintenance_requests)):
                        last_planned_date = rec._get_next_date(rec.recurring_rule_type, rec.recurring_interval,
                                                               last_planned_date)
                        vals = {
                            'plan_week': rec.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                        planning_lines_without_maintenance_requests[i].write(vals)

                        # update dates in the maintenance request
                        if planning_lines_without_maintenance_requests[i].maintenance_request_id and not \
                                planning_lines_without_maintenance_requests[i].actual_date:
                            planning_lines_without_maintenance_requests[i].maintenance_request_id.write({
                                'request_date': last_planned_date,
                                'schedule_date': last_planned_date,
                            })

                line_with_date_manually_edited.write({
                    'date_edit_mode': False
                })


class SitePlanningLine(models.Model):
    _name = 'site.planning.line'
    _rec_name = 'plan_id'
    _description = 'Site Planning Line'

    site_id = fields.Many2one(comodel_name="maintenance.equipment", required=False, ondelete="cascade")
    plan_id = fields.Many2one(comodel_name="site.planning", required=True, ondelete="cascade")
    site_name = fields.Char(string='Site Name')
    maintenance_request_id = fields.Many2one(comodel_name="maintenance.request")
    maintenance_team_id = fields.Many2one(comodel_name="maintenance.team", related='plan_id.maintenance_team_id',
                                          store=1)
    plan_week = fields.Selection(string="Week", selection=[('1', 'Week 1'), ('2', 'Week 2'),
                                                           ('3', 'Week 3'), ('4', 'Week 4'), ('5', 'Week 5')])
    date = fields.Date(string='Planned Date')
    actual_date = fields.Date(string='Actual Date', related='maintenance_request_id.starting_time_date')
    achieved = fields.Selection([('ok', 'OK'), ('not_achieved', 'Not Achieved')], string="Achieved",
                                compute='check_achieved', store=1)
    active = fields.Boolean('Active', default=True)

    date_edit_mode = fields.Boolean()

    @api.onchange('date')
    def onchange_date(self):
        self.date_edit_mode = True

    @api.depends('maintenance_request_id', 'maintenance_request_id.stage_id', 'maintenance_request_id.stage_id.done')
    def check_achieved(self):
        for rec in self:
            rec.achieved = 'not_achieved'
            if rec.maintenance_request_id and rec.maintenance_request_id.stage_id.done:
                rec.achieved = 'ok'

    def unlink(self):
        for rec in self:
            if rec.maintenance_request_id:
                raise ValidationError(
                    _('You cannot delete a maintenance planning line which has a maintenance request.'))
        return super(SitePlanningLine, self).unlink()

    @api.model
    def _cron_generate_requests_send_notifications(self):
        subtype_commit = self.env.ref("mail.mt_comment")
        planning_lines = self.env['site.planning.line'].search(
            [('date', '>=', fields.Date.today()), ('maintenance_request_id', '=', False)]).filtered(
            lambda x: (x.date - fields.Date.today()).days <= self.env.company.site_planning_notify_period)
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

    def create_new_request(self, equipment, date, planning_line):
        self.ensure_one()
        return self.env['maintenance.request'].create({
            'name': _('Preventive Full Site Maintenance - %s') % equipment.name,
            'origin': 'Preventive Full Site Maintenance',
            'request_date': date,
            'schedule_date': date,
            'maintenance_tag': 'full_site',
            'category_id': equipment.category_id.id,
            'equipment_id': equipment.id,
            'maintenance_type': 'preventive',
            'owner_user_id': equipment.owner_user_id.id,
            'user_id': equipment.technician_user_id.id,
            'maintenance_team_id': planning_line.maintenance_team_id.id,
            'duration': equipment.maintenance_duration,
            'company_id': equipment.company_id.id or self.env.company.id
        })

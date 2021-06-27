# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import timedelta


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    sla_policy_id = fields.Many2one('sla.policy', string='Type Of Issue')
    maintenance_priority = fields.Selection([('critical', 'Critical'), ('major', 'Major'), ('minor', 'Minor')],
                                            default='critical',
                                            string='Priority')

    maintenance_duration = fields.Char(string='Must Duration')
    target_dead_time = fields.Datetime(string='Target Dead Time', compute='calc_target_dead_time')

    @api.depends('maintenance_duration', 'tt_issuing_time')
    def calc_target_dead_time(self):
        for req in self:
            req.target_dead_time = False
            if req.maintenance_duration and req.tt_issuing_time:
                maintenance_duration_arr = req.maintenance_duration.split(':')
                if maintenance_duration_arr:
                    maintenance_duration_h = int(float(maintenance_duration_arr[0])) if maintenance_duration_arr[0] else 0
                    maintenance_duration_m = int(float(maintenance_duration_arr[1])) if len(maintenance_duration_arr) > 1 and maintenance_duration_arr[1] else 0
                    maintenance_duration_s = int(float(maintenance_duration_arr[2])) if len(maintenance_duration_arr) > 2 and maintenance_duration_arr[2] else 0
                    req.target_dead_time = (req.tt_issuing_time + timedelta(hours=maintenance_duration_h,
                                                                            minutes=maintenance_duration_m,
                                                                            seconds=maintenance_duration_s))

    @api.onchange('equipment_id', 'maintenance_type', 'equipment_id.category_type')
    def _set_sla_duration(self):
        for request in self:
            if request.equipment_id and request.equipment_id.category_type and request.maintenance_type == 'emergency':
                sla_lines = self.env['sla.policy.line'].sudo().search([]).filtered(
                    lambda l: l.site_category == request.equipment_id.category_type)
                if sla_lines:
                    request.maintenance_priority = sla_lines[0].priority
                    request.maintenance_duration = sla_lines[0].duration

    def action_timer_stop(self):
        for request in self:
            subtype_commit = self.env.ref("mail.mt_comment")
            res = super(MaintenanceRequest, self).action_timer_stop()
            if request.maintenance_duration and request.outage_duration_str:
                maintenance_duration_arr = request.maintenance_duration.split(':')
                maintenance_duration_h = int(float(maintenance_duration_arr[0]))
                maintenance_duration_m = int(float(maintenance_duration_arr[1]))
                maintenance_duration_s = int(float(maintenance_duration_arr[2]))
                maintenance_duration_seconds = maintenance_duration_s + maintenance_duration_m * 60 + maintenance_duration_h * 60 * 60
                outage_duration_arr = request.outage_duration_str.split(':')
                outage_duration_h = int(float(outage_duration_arr[0]))
                outage_duration_m = int(float(outage_duration_arr[1]))
                outage_duration_s = int(float(outage_duration_arr[2]))
                outage_duration_seconds = outage_duration_s + outage_duration_m * 60 + outage_duration_h * 60 * 60
                if maintenance_duration_seconds > outage_duration_seconds:
                    user = request.maintenance_team_id.team_leader_id
                    partner_ids = [user.partner_id.id]
                    request.message_post(
                        partner_ids=partner_ids,
                        subject=_('Check the maintenance request [%s] for the planning date %s') % (
                            request.name, request.request_date),
                        message_type='email',
                        subtype_id=subtype_commit.id
                    )
            return res

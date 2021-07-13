# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from odoo import http, modules, SUPERUSER_ID, tools, _


class MaintenanceRequestTimeline(models.Model):
    _name = 'maintenance.request.timeline'
    _description = 'Maintenance Request Timeline'

    start_time = fields.Datetime(string="Start Time", required=1)
    end_time = fields.Datetime(string="End Time")
    duration = fields.Float(string="Duration (hours)", compute='_get_duration', store=1)
    duration_str = fields.Char(string="Duration", compute='_get_duration', store=1)
    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request', required=True)

    @api.constrains('start_time', 'end_time')
    def check_time(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.end_time < rec.start_time:
                raise ValidationError(_("Start time should be prior to end time."))

    @api.depends('start_time', 'end_time')
    def _get_duration(self):
        for rec in self:
            if not rec.start_time or not rec.end_time:
                rec.duration = 0
                rec.duration_str = '00:00:00'
            else:
                timedelta = rec.end_time - rec.start_time
                timedelta_in_seconds = timedelta.days * 24 * 3600 + timedelta.seconds
                minutes, seconds = divmod(timedelta_in_seconds, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)

                hours = str(int(hours)) if hours else '00'
                minutes = str(int(minutes)) if minutes else '00'
                seconds = str(int(seconds)) if seconds else '00'
                hours_str = '0' + hours if len(hours) == 1 else hours
                minutes_str = '0' + minutes if len(minutes) == 1 else minutes
                seconds_str = '0' + seconds if len(seconds) == 1 else seconds
                duration_str = hours_str + ':' + minutes_str + ':' + seconds_str
                if days:
                    duration_str = str(days) + ' days / ' + duration_str
                rec.duration_str = duration_str
                rec.duration = timedelta_in_seconds / 3600

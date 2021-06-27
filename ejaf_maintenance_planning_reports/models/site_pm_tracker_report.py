# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SitePmTrackerReport(models.TransientModel):
    _name = 'site.pm.tracker.report'
    _description = 'Site PM Tracker Report'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    def print_site_pm_tracker_report(self):
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValidationError("Date to must greater than date from")
        data = {'date_from': self.date_from, 'date_to': self.date_to}
        return self.env['ir.actions.report'].search(
            [('report_name', '=', 'ejaf_maintenance_planning_reports.site_pm_reports'),
             ('report_type', '=', 'xlsx')],
            limit=1).report_action(self, data=data)

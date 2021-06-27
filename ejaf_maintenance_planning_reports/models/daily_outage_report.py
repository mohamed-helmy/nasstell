# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DailyOutageReport(models.TransientModel):
    _name = 'daily.outage.report'
    _description = 'Daily Outage Report'

    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')

    def print_daily_outage_report(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must less than to date")
        data = {'from_date': self.from_date, 'to_date': self.to_date}
        return self.env['ir.actions.report'].search(
            [('report_name', '=', 'ejaf_maintenance_planning_reports.daily_outage_report'),
             ('report_type', '=', 'xlsx')],
            limit=1).report_action(self, data=data)

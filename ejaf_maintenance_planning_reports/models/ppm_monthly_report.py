# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

MONTHS = [('1', "January"),
          ('2', "February"),
          ('3', "March"),
          ('4', "April"),
          ('5', "May"),
          ('6', "June"),
          ('7', "July"),
          ('8', "August"),
          ('9', "September"),
          ('10', "October"),
          ('11', "November"),
          ('12', "December")]


class PpmMonthlyReport(models.TransientModel):
    _name = 'ppm.monthly.report'
    _description = 'PPM Monthly Report'

    def get_year_selection(self):
        current_year = int(datetime.now().year)
        year_lst = [(str(current_year), str(current_year))]
        for item in range(1, 10):
            year_lst.append(
                (str(current_year - item), str(current_year - item))
            )
        return year_lst

    report_type = fields.Selection([('summary', 'Summary'), ('activity', 'Activity')], default='activity',
                                   string='Report Type')
    month = fields.Selection(MONTHS, string='Month')
    year = fields.Selection(selection=get_year_selection, string='Year')
    region_ids = fields.Many2many('region', string='Regions')
    group_by_group = fields.Boolean(string='Select Group By Group', default=True)

    def print_ppm_monthly_reports(self):
        data = {'report_type': self.report_type, 'month': self.month if self.month else False,
                'year': self.year if self.year else False,
                'region_ids': self.region_ids.ids if self.region_ids else False, 'group_by_group': self.group_by_group}
        return self.env['ir.actions.report'].search(
            [('report_name', '=', 'ejaf_maintenance_planning_reports.ppm_reports'),
             ('report_type', '=', 'xlsx')],
            limit=1).report_action(self, data=data)

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


class FuelAnalysisReport(models.TransientModel):
    _name = 'fuel.analysis.report'
    _description = 'Fuel Analysis Report'

    def get_year_selection(self):
        current_year = int(datetime.now().year)
        year_lst = [(str(current_year), str(current_year))]
        for item in range(1, 10):
            year_lst.append(
                (str(current_year - item), str(current_year - item))
            )
        return year_lst

    month = fields.Selection(MONTHS, string='Month')
    year = fields.Selection(selection=get_year_selection, string='Year')
    report_type = fields.Selection(
        [('fuel_plan', 'Fuel Plan'), ('fuel_analysis', 'Fuel Analysis'), ('fuel_distribution', 'Fuel Distribution')])

    def print_fuel_analysis_report(self):
        data = {'report_type': self.report_type if self.report_type else False,
                'month': self.month if self.month else False,
                'year': self.year if self.year else False}
        return self.env['ir.actions.report'].search(
            [('report_name', '=', 'ejaf_maintenance_planning_reports.fuel_analysis_reports'),
             ('report_type', '=', 'xlsx')],
            limit=1).report_action(self, data=data)

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


class MaintenancePlanningReports(models.TransientModel):
    _name = 'maintenance.planning.reports'
    _description = 'Maintenance Planning Reports'

    def get_year_selection(self):
        current_year = int(datetime.now().year)
        year_lst = [(str(current_year), str(current_year))]
        for item in range(1, 10):
            year_lst.append(
                (str(current_year - item), str(current_year - item))
            )
        return year_lst

    planning_type = fields.Selection([('summary', 'Summary'), ('by_month', 'By Month')],
                                     string='Planning Type', default='by_month')
    month = fields.Selection(MONTHS, string='Month')
    year = fields.Selection(selection=get_year_selection, string='Year')
    site_plan = fields.Boolean()

    def print_reports(self):
        data = {'site_plan': self.site_plan, 'planning_type': self.planning_type,
                'month': self.month if self.month else False,
                'year': self.year if self.year else False}
        return self.env['ir.actions.report'].search(
            [('report_name', '=', 'ejaf_maintenance_planning_reports.maintenance_reports'),
             ('report_type', '=', 'xlsx')],
            limit=1).report_action(self, data=data)


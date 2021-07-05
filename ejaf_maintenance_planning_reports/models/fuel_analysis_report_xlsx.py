# -*- coding: utf-8 -*-
import base64
import io

from odoo import models
from datetime import date
import calendar
from datetime import timedelta

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


class FuelAnalysisReportXlsx(models.AbstractModel):
    _name = 'report.ejaf_maintenance_planning_reports.fuel_analysis_reports'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_data):
        f1 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 16})
        f2 = workbook.add_format(
            {'bold': True, 'font_color': '#ffffff', 'align': 'center', 'font_size': 10, 'bg_color': '#310a7e',
             'border': True})
        f22 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 10, 'bg_color': '#96bbcd',
             'border': True})
        f3 = workbook.add_format(
            {'bold': False, 'font_color': '#000000', 'align': 'center', 'bg_color': '#ffffff', 'font_size': 10,
             'border': True})
        if data['report_type'] == 'fuel_analysis':
            worksheet = workbook.add_worksheet("Fuel Analysis Report")
            buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
            image_width = 340.0
            image_height = 140.0

            cell_width = 64.0
            cell_height = 20.0

            x_scale = cell_width / image_width
            y_scale = cell_height / image_height

            worksheet.insert_image('A1:C1', "any_name.png",
                                   {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            year = int(data['year'])
            month = int(data['month'])
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            worksheet.merge_range('A2:B3', 'Fuel Analysis #' + str(month), f1)
            worksheet.set_column('A2:B3', 20)
            row = 4
            worksheet.write(row, 0, '#', f2)
            worksheet.write(row, 1, 'Site ID', f2)
            worksheet.set_column(row, 1, 20)
            worksheet.write(row, 2, 'Site Name', f2)
            worksheet.set_column(row, 2, 20)
            worksheet.write(row, 3, 'Last Visit', f2)
            worksheet.set_column(row, 3, 20)
            worksheet.write(row, 4, 'G1RH', f2)
            worksheet.set_column(row, 4, 20)
            worksheet.write(row, 5, 'G2RH', f2)
            worksheet.set_column(row, 5, 20)
            worksheet.write(row, 6, 'Total', f2)
            worksheet.set_column(row, 6, 20)
            worksheet.write(row, 7, 'Days', f2)
            worksheet.set_column(row, 7, 20)
            worksheet.write(row, 8, 'Letters Per Hour', f2)
            worksheet.set_column(row, 8, 20)
            worksheet.write(row, 9, 'R.H / day', f2)
            worksheet.set_column(row, 9, 20)
            worksheet.write(row, 10, 'Tank Size', f2)
            worksheet.set_column(row, 10, 20)
            worksheet.write(row, 11, 'Remain days before the next visit', f2)
            worksheet.set_column(row, 11, 20)
            worksheet.write(row, 12, 'Remain letters in the tank', f2)
            worksheet.set_column(row, 12, 20)
            worksheet.write(row, 13, 'C.P Status', f2)
            worksheet.set_column(row, 13, 20)
            worksheet.write(row, 14, 'Plan for the next visit', f2)
            worksheet.set_column(row, 14, 20)
            row += 1
            number = 1
            sites = []
            for request in self.env['maintenance.request'].search(
                    [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'fuel_planning'),
                     ('starting_time', '!=', False)],order="starting_time desc"):
                if request.equipment_id:
                    worksheet.write(row, 0, str(number), f22)
                    worksheet.write(row, 1,
                                    str(request.equipment_id.site) if request.equipment_id and request.equipment_id.site else '',
                                    f22)
                    worksheet.set_column(row, 1, 20)
                    worksheet.write(row, 2,
                                    str(request.equipment_id.name) if request.equipment_id and request.equipment_id.name else '',
                                    f22)
                    worksheet.set_column(row, 2, 20)
                    worksheet.write(row, 3,
                                    str(request.starting_time) if request.starting_time and start_date <= request.starting_time.date() <= end_date else '',
                                    f3)
                    worksheet.set_column(row, 3, 20)
                    worksheet.write(row, 4,
                                    str(request.g1rh_analysis) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.g1rh_analysis else '0',
                                    f3)
                    worksheet.set_column(row, 4, 20)
                    worksheet.write(row, 5,
                                    str(request.g2rh_analysis) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.g2rh_analysis else '0',
                                    f3)
                    worksheet.set_column(row, 5, 20)

                    worksheet.write(row, 6,
                                    str(request.total_rhs) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.total_rhs else '0',
                                    f3)
                    worksheet.set_column(row, 6, 20)
                    worksheet.write(row, 7,
                                    str(request.days) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.days else '0',
                                    f3)
                    worksheet.set_column(row, 7, 20)
                    worksheet.write(row, 8,
                                    str(request.liters_per_hour) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.liters_per_hour else '0',
                                    f3)
                    worksheet.set_column(row, 8, 20)

                    worksheet.write(row, 9,
                                    str(request.rh_per_day) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.rh_per_day else '0',
                                    f3)
                    worksheet.set_column(row, 9, 20)
                    worksheet.write(row, 10,
                                    str(request.tank_size) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.tank_size else '0',
                                    f3)
                    worksheet.set_column(row, 10, 20)
                    remain_days = 0
                    worksheet.write(row, 11,
                                    str(request.remaining_days_before_next_visit) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.remaining_days_before_next_visit else '0',
                                    f3)
                    worksheet.write(row, 12,
                                    str(request.remain_letters if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.remain_letters else '0'),
                                    f3)
                    worksheet.set_column(row, 12, 20)

                    worksheet.write(row, 13,
                                    str(request.c_p_status) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.c_p_status else '',
                                    f3)
                    worksheet.set_column(row, 13, 20)
                    worksheet.write(row, 14,
                                    str(request.next_visit_plan) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.next_visit_plan else '',
                                    f3)
                    worksheet.set_column(row, 14, 20)
                    site_fuel_lines = self.env['fuel.planning.line'].sudo().search(
                        [('site_id', '=', request.equipment_id.id), ('date', '>=', start_date),
                         ('date', '<=', end_date)])
                    for line in site_fuel_lines:
                        line.remain_letters_in_the_tank = request.remain_letters
                        line.maintenance_request_id = request.id
                        line.date = request.next_visit_plan
                    row += 1
        if data['report_type'] == 'fuel_plan':
            worksheet = workbook.add_worksheet("Fuel Plan Report")
            buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
            image_width = 340.0
            image_height = 140.0

            cell_width = 64.0
            cell_height = 20.0

            x_scale = cell_width / image_width
            y_scale = cell_height / image_height

            worksheet.insert_image('A1:C1', "any_name.png",
                                   {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            year = int(data['year'])
            month = int(data['month'])
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            worksheet.merge_range('D2:F3', 'Fuel Plan #' + str(month), f1)
            worksheet.set_column('D2:F3', 20)
            row = 4
            worksheet.write(row, 0, '#', f2)
            worksheet.write(row, 1, 'Site ID', f2)
            worksheet.set_column(row, 1, 20)
            worksheet.write(row, 2, 'Site Name', f2)
            worksheet.set_column(row, 2, 20)
            worksheet.write(row, 3, 'Last Visit', f2)
            worksheet.set_column(row, 3, 20)
            worksheet.write(row, 4, 'Remain letters in the tank', f2)
            worksheet.set_column(row, 4, 20)
            worksheet.write(row, 5, 'Plan for the next visit', f2)
            worksheet.set_column(row, 5, 20)
            row += 1
            number = 1
            for request in self.env['maintenance.request'].search(
                    [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'fuel_planning'),
                     ('starting_time', '!=', False)], order="starting_time desc"):
                if request.starting_time and start_date <= request.starting_time.date() <= end_date:
                    worksheet.write(row, 0, str(number), f22)
                    worksheet.write(row, 1, str(request.equipment_id.site) if request.equipment_id and request.equipment_id.site else '', f22)
                    worksheet.set_column(row, 1, 20)
                    worksheet.write(row, 2, str(request.equipment_id.name) if request.equipment_id and request.equipment_id.name else '', f22)
                    worksheet.set_column(row, 2, 20)
                    worksheet.write(row, 3,
                                    str(request.starting_time) if request.starting_time and request.starting_time else '',
                                    f3)
                    worksheet.set_column(row, 3, 20)
                    worksheet.write(row, 4,
                                    str(request.remain_letters if request.remain_letters else ''),
                                    f3)
                    worksheet.set_column(row, 4, 20)

                    worksheet.write(row, 5,
                                    str(request.next_visit_plan) if request.next_visit_plan else '',
                                    f3)
                    worksheet.set_column(row, 5, 20)

                number += 1
        if data['report_type'] == 'fuel_distribution':
            worksheet = workbook.add_worksheet("Fuel Distribution Report")
            buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
            image_width = 340.0
            image_height = 140.0

            cell_width = 64.0
            cell_height = 20.0

            x_scale = cell_width / image_width
            y_scale = cell_height / image_height

            worksheet.insert_image('A1:C1', "any_name.png",
                                   {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            year = int(data['year'])
            month = int(data['month'])
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            worksheet.merge_range('A2:C3', 'Fuel Distribution #' + str(month), f1)
            worksheet.set_column('A2:C3', 20)
            row = 4
            ff = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 10, 'bg_color': '#a5adb0',
                 'border': True})
            ff1 = workbook.add_format(
                {'bold': False, 'font_color': '#000000', 'align': 'center', 'font_size': 10, 'bg_color': '#ffffff',
                 'border': True})
            worksheet.write(row, 0, 'Site ID', ff)
            worksheet.set_column(row, 0, 20)
            worksheet.write(row, 1, 'Site Name', ff)
            worksheet.set_column(row, 1, 20)
            worksheet.write(row, 2, 'Provide Date', ff)
            worksheet.set_column(row, 2, 20)
            worksheet.write(row, 3, 'Liters in the tank', ff)
            worksheet.set_column(row, 3, 20)
            worksheet.write(row, 4, 'Filling liters', ff)
            worksheet.set_column(row, 4, 20)
            worksheet.write(row, 5, 'Total liters', ff)
            worksheet.set_column(row, 5, 20)
            worksheet.write(row, 6, 'Tank size', ff)
            worksheet.set_column(row, 6, 20)
            worksheet.write(row, 7, 'G1RH', ff)
            worksheet.set_column(row, 7, 20)
            worksheet.write(row, 8, 'G2RH', ff)
            worksheet.set_column(row, 8, 20)
            worksheet.write(row, 9, 'C.P Status', ff)
            worksheet.set_column(row, 9, 20)
            row += 1
            for request in self.env['maintenance.request'].search(
                    [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'fuel_planning'),
                     ('starting_time', '!=', False)], order="starting_time desc"):
                if request.equipment_id:
                    worksheet.write(row, 0,
                                    str(request.equipment_id.site) if request.equipment_id and request.equipment_id.site else '',
                                    ff1)
                    worksheet.set_column(row, 0, 20)
                    worksheet.write(row, 1,
                                    str(request.equipment_id.name) if request.equipment_id and request.equipment_id.name else '',
                                    ff1)
                    worksheet.set_column(row, 1, 20)
                    worksheet.write(row, 2,
                                    str(request.starting_time) if request.starting_time and start_date <= request.starting_time.date() <= end_date else '',
                                    ff1)
                    worksheet.set_column(row, 2, 20)
                    worksheet.write(row, 3,
                                    str(request.liters_in_the_tank) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.liters_in_the_tank else '0',
                                    ff1)
                    worksheet.set_column(row, 3, 20)
                    worksheet.write(row, 4,
                                    str(request.filling_liters) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.filling_liters else '0',
                                    ff1)
                    worksheet.set_column(row, 4, 20)

                    worksheet.write(row, 5,
                                    str(request.total_liters) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.total_liters else '0',
                                    ff1)
                    worksheet.set_column(row, 5, 20)

                    worksheet.write(row, 6,
                                    str(request.tank_size) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.tank_size else '0',
                                    ff1)
                    worksheet.set_column(row, 6, 20)

                    worksheet.write(row, 7,
                                    str(request.g1rh) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.g1rh else '0',
                                    ff1)
                    worksheet.set_column(row, 7, 20)

                    worksheet.write(row, 8,
                                    str(request.g2rh) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.g2rh else '0',
                                    ff1)
                    worksheet.set_column(row, 8, 20)
                    worksheet.write(row, 9,
                                    str(request.c_p_status) if request.starting_time and start_date <= request.starting_time.date() <= end_date and request.c_p_status else '',
                                    ff1)
                    worksheet.set_column(row, 9, 20)
                    row += 1

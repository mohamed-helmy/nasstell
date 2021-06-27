# -*- coding: utf-8 -*-
import base64
import io

from odoo import models
from datetime import date
import calendar

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


class PPMMonthlyReportXlsx(models.AbstractModel):
    _name = 'report.ejaf_maintenance_planning_reports.ppm_reports'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_data):
        worksheet = workbook.add_worksheet("PPM Monthly Report")
        f1 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 16, 'border': True})
        f11 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 12, 'bg_color': '#8d93bf',
             'border': True})
        f2 = workbook.add_format(
            {'bold': False, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#0d1c7a', 'border': True})
        f4 = workbook.add_format(
            {'bold': True, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#0d1c7a', 'font_size': 10,
             'border': True})
        f5 = workbook.add_format(
            {'bold': False, 'font_color': '#000000', 'align': 'center', 'bg_color': '#c2c5df', 'font_size': 10,
             'border': True})
        f55 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'bg_color': '#c2c5df', 'font_size': 10,
             'border': True})
        f6 = workbook.add_format(
            {'bold': False, 'font_color': '#000000', 'align': 'center', 'bg_color': '#ffffff', 'font_size': 10,
             'border': True})
        f3 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'bg_color': '#c91f43', 'border': True})
        buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        image_width = 340.0
        image_height = 140.0

        cell_width = 64.0
        cell_height = 20.0

        x_scale = cell_width / image_width
        y_scale = cell_height / image_height

        worksheet.insert_image('A1', "any_name.png", {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
        year = int(data['year'])
        month = int(data['month'])
        if data['report_type'] == 'summary':
            if data['report_type'] == 'summary':
                month_days = calendar.monthrange(year, month)[1]
                region_ids = data['region_ids']
                group_by_group = data['group_by_group']
                start_date = date(year, month, 1)
                last_day = calendar.monthrange(year, month)[1]
                end_date = date(year, month, last_day)
                remaining = month_days - 28
                worksheet.merge_range('A3:C4', 'Summary of PPM Monthly Report #' + str(month), f1)
                worksheet.set_column('A3:C4', 20)
                worksheet.merge_range('A5:N5', 'Month #' + str(month), f3)
                worksheet.set_column('A5:N5', 20)
                worksheet.merge_range('A6:B6', 'Summary', f3)
                worksheet.set_column('A6:B6', 20)
                worksheet.merge_range('C6:D6', 'Week #1 (1-7)', f3)
                worksheet.set_column('C6:D6', 20)
                worksheet.merge_range('E6:F6', 'Week #2 (8-14)', f3)
                worksheet.set_column('E6:F6', 20)
                worksheet.merge_range('G6:H6', 'Week #3 (15-21)', f3)
                worksheet.set_column('G6:H6', 20)
                worksheet.merge_range('I6:J6', 'Week #4 (22-28)', f3)
                worksheet.set_column('I6:J6', 20)
                if remaining:
                    worksheet.merge_range('K6:L6', 'Remain Days (29-' + str(month_days) + ')', f3)
                    worksheet.set_column('K6:L6', 20)
                    worksheet.merge_range('M6:N6', 'Total', f3)
                    worksheet.set_column('M6:N6', 20)
                else:
                    worksheet.merge_range('K6:L6', 'Total', f3)
                    worksheet.set_column('K6:L6', 20)
                col = 1
                if group_by_group:
                    worksheet.write(6, 0, 'Region', f2)
                    worksheet.set_column(6, 0, 20)
                    worksheet.write(6, 1, 'Group', f2)
                    worksheet.set_column(6, 1, 20)
                else:
                    worksheet.merge_range('A6:B7', 'Region', f2)
                    worksheet.set_column('A6:B7', 20)
                col += 1
                worksheet.write(6, col, 'Planned', f2)
                worksheet.set_column(6, col, 20)
                worksheet.write(6, col + 1, 'Achieved', f2)
                worksheet.set_column(6, col + 1, 20)
                worksheet.write(6, col + 2, 'Planned', f2)
                worksheet.set_column(6, col + 2, 20)
                worksheet.write(6, col + 3, 'Achieved', f2)
                worksheet.set_column(6, col + 3, 20)
                worksheet.write(6, col + 4, 'Planned', f2)
                worksheet.set_column(6, col + 4, 20)
                worksheet.write(6, col + 5, 'Achieved', f2)
                worksheet.set_column(6, col + 5, 20)
                worksheet.write(6, col + 6, 'Planned', f2)
                worksheet.set_column(6, col + 6, 20)
                worksheet.write(6, col + 7, 'Achieved', f2)
                worksheet.set_column(6, col + 7, 20)
                if remaining:
                    worksheet.write(6, col + 8, 'Planned', f2)
                    worksheet.set_column(6, col + 8, 20)
                    worksheet.write(6, col + 9, 'Achieved', f2)
                    worksheet.set_column(6, col + 9, 20)
                    worksheet.write(6, col + 10, 'Planned', f2)
                    worksheet.set_column(6, col + 10, 20)
                    worksheet.write(6, col + 11, 'Achieved', f2)
                    worksheet.set_column(6, col + 11, 20)
                else:
                    worksheet.write(6, col + 8, 'Planned', f2)
                    worksheet.set_column(6, col + 8, 20)
                    worksheet.write(6, col + 9, 'Achieved', f2)
                    worksheet.set_column(6, col + 9, 20)
                row = 7
                for region in region_ids:
                    region_obj = self.env['region'].sudo().browse(region)

                    region_generator_planning_lines = self.env['generator.planning.line'].sudo().search(
                        [('date', '>=', start_date), ('date', '<=', end_date), ('site_id.region_id', '=', region)])
                    col = 1
                    if group_by_group:
                        week1_data_center_planned = region_generator_planning_lines.filtered(
                            lambda l: 1 <= l.date.day <= 7 and l.site_id.group == 'data_center')
                        week1_data_center_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 1 <= l.date.day <= 7 and l.site_id.group == 'data_center' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week1_major_planned = region_generator_planning_lines.filtered(
                            lambda l: 1 <= l.date.day <= 7 and l.site_id.group == 'major')
                        week1_major_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 1 <= l.date.day <= 7 and l.site_id.group == 'major' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week1_normal_planned = region_generator_planning_lines.filtered(
                            lambda l: 1 <= l.date.day <= 7 and l.site_id.group == 'normal')
                        week1_normal_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 1 <= l.date.day <= 7 and l.site_id.group == 'normal' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        total_week1_planned = len(week1_data_center_planned) + len(week1_major_planned) + len(
                            week1_normal_planned)
                        total_week1_achieved = len(week1_data_center_achieved) + len(week1_major_achieved) + len(
                            week1_normal_achieved)
                        week2_data_center_planned = region_generator_planning_lines.filtered(
                            lambda l: 8 <= l.date.day <= 15 and l.site_id.group == 'data_center')
                        week2_data_center_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 8 <= l.date.day <= 15 and l.site_id.group == 'data_center' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week2_major_planned = region_generator_planning_lines.filtered(
                            lambda l: 8 <= l.date.day <= 15 and l.site_id.group == 'major')
                        week2_major_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 8 <= l.date.day <= 15 and l.site_id.group == 'major' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week2_normal_planned = region_generator_planning_lines.filtered(
                            lambda l: 8 <= l.date.day <= 15 and l.site_id.group == 'normal')
                        week2_normal_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 8 <= l.date.day <= 15 and l.site_id.group == 'normal' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        total_week2_planned = len(week2_data_center_planned) + len(week2_major_planned) + len(
                            week2_normal_planned)
                        total_week2_achieved = len(week2_data_center_achieved) + len(week2_major_achieved) + len(
                            week2_normal_achieved)
                        week3_data_center_planned = region_generator_planning_lines.filtered(
                            lambda l: 16 <= l.date.day <= 21 and l.site_id.group == 'data_center')
                        week3_data_center_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 16 <= l.date.day <= 21 and l.site_id.group == 'data_center' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week3_major_planned = region_generator_planning_lines.filtered(
                            lambda l: 16 <= l.date.day <= 21 and l.site_id.group == 'major')
                        week3_major_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 16 <= l.date.day <= 21 and l.site_id.group == 'major' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week3_normal_planned = region_generator_planning_lines.filtered(
                            lambda l: 16 <= l.date.day <= 21 and l.site_id.group == 'normal')
                        week3_normal_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 16 <= l.date.day <= 21 and l.site_id.group == 'normal' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        total_week3_planned = len(week3_data_center_planned) + len(week3_major_planned) + len(
                            week3_normal_planned)
                        total_week3_achieved = len(week3_data_center_achieved) + len(week3_major_achieved) + len(
                            week3_normal_achieved)
                        week4_data_center_planned = region_generator_planning_lines.filtered(
                            lambda l: 22 <= l.date.day <= 28 and l.site_id.group == 'data_center')
                        week4_data_center_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 22 <= l.date.day <= 28 and l.site_id.group == 'data_center' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week4_major_planned = region_generator_planning_lines.filtered(
                            lambda l: 22 <= l.date.day <= 28 and l.site_id.group == 'major')
                        week4_major_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 22 <= l.date.day <= 28 and l.site_id.group == 'major' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week4_normal_planned = region_generator_planning_lines.filtered(
                            lambda l: 22 <= l.date.day <= 28 and l.site_id.group == 'normal')
                        week4_normal_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 22 <= l.date.day <= 28 and l.site_id.group == 'normal' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        total_week4_planned = len(week4_data_center_planned) + len(week4_major_planned) + len(
                            week4_normal_planned)
                        total_week4_achieved = len(week4_data_center_achieved) + len(week4_major_achieved) + len(
                            week4_normal_achieved)
                        total_data_center_planned = len(week1_data_center_planned) + len(
                            week2_data_center_planned) + len(
                            week3_data_center_planned) + len(week4_data_center_planned)
                        total_data_center_achieved = len(week1_data_center_achieved) + len(
                            week2_data_center_achieved) + len(
                            week3_data_center_achieved) + len(week4_data_center_achieved)
                        total_major_planned = len(week1_major_planned) + len(week2_major_planned) + len(
                            week3_major_planned) + len(week4_major_planned)
                        total_major_achieved = len(week1_major_achieved) + len(week2_major_achieved) + len(
                            week3_major_achieved) + len(week4_major_achieved)
                        total_normal_planned = len(week1_normal_planned) + len(week2_normal_planned) + len(
                            week3_normal_planned) + len(week4_normal_planned)
                        total_normal_achieved = len(week1_normal_achieved) + len(week2_normal_achieved) + len(
                            week3_normal_achieved) + len(week4_normal_achieved)
                        region_range = 'A' + str(row + 1) + ':A' + str(row + 4)
                        worksheet.merge_range(region_range, region_obj.name, f2)
                        worksheet.set_column(region_range, 20)
                        worksheet.write(row, 1, 'Data Center', f2)
                        worksheet.write(row + 1, 1, 'Major', f2)
                        worksheet.write(row + 2, 1, 'Normal', f2)
                        worksheet.write(row + 3, 1, 'Total', f2)
                        worksheet.set_column(row, 1, 20)
                        worksheet.set_column(row + 1, 1, 20)
                        worksheet.set_column(row + 2, 1, 20)
                        worksheet.set_column(row + 3, 1, 20)
                        col += 1
                        # data center group
                        worksheet.write(row, col,
                                        str(len(week1_data_center_planned)) if week1_data_center_planned else '0',
                                        f2)
                        worksheet.set_column(row, col, 20)
                        worksheet.write(row, col + 1,
                                        str(len(week1_data_center_achieved)) if week1_data_center_achieved else '0', f2)
                        worksheet.set_column(row, col + 1, 20)
                        worksheet.write(row, col + 2,
                                        str(len(week2_data_center_planned)) if week2_data_center_planned else '0', f2)
                        worksheet.set_column(row, col + 2, 20)
                        worksheet.write(row, col + 3,
                                        str(len(week2_data_center_achieved)) if week2_data_center_achieved else '0', f2)
                        worksheet.set_column(row, col + 3, 20)
                        worksheet.write(row, col + 4,
                                        str(len(week3_data_center_planned)) if week3_data_center_planned else '0', f2)
                        worksheet.set_column(row, col + 4, 20)
                        worksheet.write(row, col + 5,
                                        str(len(week3_data_center_achieved)) if week3_data_center_achieved else '0', f2)
                        worksheet.set_column(row, col + 5, 20)
                        worksheet.write(row, col + 6,
                                        str(len(week4_data_center_planned)) if week4_data_center_planned else '0', f2)
                        worksheet.set_column(row, col + 6, 20)
                        worksheet.write(row, col + 7,
                                        str(len(week4_data_center_achieved)) if week4_data_center_achieved else '0', f2)
                        worksheet.set_column(row, col + 7, 20)
                        # Major group
                        worksheet.write(row + 1, col, str(len(week1_major_planned)) if week1_major_planned else '0', f2)
                        worksheet.set_column(row + 1, col, 20)
                        worksheet.write(row + 1, col + 1,
                                        str(len(week1_major_achieved)) if week1_major_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 1, 20)
                        worksheet.write(row + 1, col + 2, str(len(week2_major_planned)) if week2_major_planned else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 2, 20)
                        worksheet.write(row + 1, col + 3,
                                        str(len(week2_major_achieved)) if week2_major_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 3, 20)
                        worksheet.write(row + 1, col + 4, str(len(week3_major_planned)) if week3_major_planned else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 4, 20)
                        worksheet.write(row + 1, col + 5,
                                        str(len(week3_major_achieved)) if week3_major_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 5, 20)
                        worksheet.write(row + 1, col + 6, str(len(week4_major_planned)) if week4_major_planned else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 6, 20)
                        worksheet.write(row + 1, col + 7,
                                        str(len(week4_major_achieved)) if week4_major_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 1, col + 7, 20)
                        # Normal group
                        worksheet.write(row + 2, col, str(len(week1_normal_planned)) if week1_normal_planned else '0',
                                        f2)
                        worksheet.set_column(row + 2, col, 20)
                        worksheet.write(row + 2, col + 1,
                                        str(len(week1_normal_achieved)) if week1_normal_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 1, 20)
                        worksheet.write(row + 2, col + 2,
                                        str(len(week2_normal_planned)) if week2_normal_planned else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 2, 20)
                        worksheet.write(row + 2, col + 3,
                                        str(len(week2_normal_achieved)) if week2_normal_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 3, 20)
                        worksheet.write(row + 2, col + 4,
                                        str(len(week3_normal_planned)) if week3_normal_planned else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 4, 20)
                        worksheet.write(row + 2, col + 5,
                                        str(len(week3_normal_achieved)) if week3_normal_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 5, 20)
                        worksheet.write(row + 2, col + 6,
                                        str(len(week4_normal_planned)) if week4_normal_planned else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 6, 20)
                        worksheet.write(row + 2, col + 7,
                                        str(len(week4_normal_achieved)) if week4_normal_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 2, col + 7, 20)
                        # Total
                        worksheet.write(row + 3, col, str(total_week1_planned) if total_week1_planned else '0', f2)
                        worksheet.set_column(row + 3, col, 20)
                        worksheet.write(row + 3, col + 1, str(total_week1_achieved) if week1_normal_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 1, 20)
                        worksheet.write(row + 3, col + 2, str(total_week2_planned) if total_week2_planned else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 2, 20)
                        worksheet.write(row + 3, col + 3, str(total_week2_achieved) if total_week2_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 3, 20)
                        worksheet.write(row + 3, col + 4, str(total_week3_planned) if total_week3_planned else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 4, 20)
                        worksheet.write(row + 3, col + 5, str(total_week3_achieved) if total_week3_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 5, 20)
                        worksheet.write(row + 3, col + 6, str(total_week4_planned) if total_week4_planned else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 6, 20)
                        worksheet.write(row + 3, col + 7, str(total_week4_achieved) if total_week4_achieved else '0',
                                        f2)
                        worksheet.set_column(row + 3, col + 7, 20)
                        if remaining:
                            col = 10

                            remaining_data_center_planned = region_generator_planning_lines.filtered(
                                lambda l: 29 <= l.date.day <= month_days and l.site_id.group == 'data_center')
                            remaining_data_center_achieved = region_generator_planning_lines.filtered(
                                lambda
                                    l: 29 <= l.date.day <= month_days and l.site_id.group == 'data_center' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                            remaining_major_planned = region_generator_planning_lines.filtered(
                                lambda l: 29 <= l.date.day <= month_days and l.site_id.group == 'major')
                            remaining_major_achieved = region_generator_planning_lines.filtered(
                                lambda
                                    l: 29 <= l.date.day <= month_days and l.site_id.group == 'major' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                            remaining_normal_planned = region_generator_planning_lines.filtered(
                                lambda l: 29 <= l.date.day <= month_days and l.site_id.group == 'normal')
                            remaining_normal_achieved = region_generator_planning_lines.filtered(
                                lambda
                                    l: 29 <= l.date.day <= month_days and l.site_id.group == 'normal' and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)

                            # Remaining
                            worksheet.write(row, col, str(len(
                                remaining_data_center_planned)) if remaining_data_center_planned else '0', f2)
                            worksheet.set_column(row, col, 20)
                            worksheet.write(row, col + 1,
                                            str(len(
                                                remaining_data_center_achieved)) if remaining_data_center_achieved else '0',
                                            f2)
                            worksheet.set_column(row, col + 1, 20)
                            worksheet.write(row + 1, col,
                                            str(len(remaining_major_planned)) if remaining_major_planned else '0',
                                            f2)
                            worksheet.set_column(row + 1, col, 20)
                            worksheet.write(row + 1, col + 1,
                                            str(len(remaining_major_achieved)) if remaining_major_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 1, col + 1, 20)
                            worksheet.write(row + 2, col,
                                            str(len(remaining_normal_planned)) if remaining_normal_planned else '0',
                                            f2)
                            worksheet.set_column(row + 2, col, 20)
                            worksheet.write(row + 2, col + 1,
                                            str(len(remaining_normal_achieved)) if remaining_normal_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 2, col + 1, 20)
                            # Total Of Total
                            total_data_center_planned += len(remaining_data_center_planned)
                            total_data_center_achieved += len(remaining_data_center_achieved)
                            total_major_planned += len(remaining_major_planned)
                            total_major_achieved += len(remaining_major_achieved)
                            total_normal_planned += len(remaining_normal_planned)
                            total_normal_achieved += len(remaining_normal_achieved)

                            worksheet.write(row, col + 2,
                                            str(total_data_center_planned) if total_data_center_planned else '0', f2)
                            worksheet.set_column(row, col + 2, 20)
                            worksheet.write(row, col + 3,
                                            str(total_data_center_achieved) if total_data_center_achieved else '0',
                                            f2)
                            worksheet.set_column(row, col + 3, 20)
                            worksheet.write(row + 1, col + 2,
                                            str(total_major_planned) if total_major_planned else '0',
                                            f2)
                            worksheet.set_column(row + 1, col + 2, 20)
                            worksheet.write(row + 1, col + 3,
                                            str(total_major_achieved) if total_major_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 1, col + 3, 20)
                            worksheet.write(row + 2, col + 2,
                                            str(total_normal_planned) if total_normal_planned else '0',
                                            f2)
                            worksheet.set_column(row + 2, col + 2, 20)
                            worksheet.write(row + 2, col + 3,
                                            str(total_normal_achieved) if total_normal_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 2, col + 3, 20)
                            total_planned = total_data_center_planned + total_major_planned + total_normal_planned
                            total_achieved = total_data_center_achieved + total_major_achieved + total_normal_achieved
                            worksheet.write(row + 3, col + 2,
                                            str(total_planned) if total_planned else '0',
                                            f2)
                            worksheet.set_column(row + 3, col + 2, 20)
                            worksheet.write(row + 3, col + 3,
                                            str(total_achieved) if total_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 3, col + 3, 20)

                            # Total Remaining
                            total_remaining_planned = len(remaining_data_center_planned) + len(
                                remaining_major_planned) + len(remaining_normal_planned)
                            total_remaining_achieved = len(remaining_data_center_achieved) + len(
                                remaining_normal_achieved) + len(remaining_major_achieved)
                            worksheet.write(row + 3, col,
                                            str(total_remaining_planned) if total_remaining_planned else '0',
                                            f2)
                            worksheet.set_column(row + 3, col, 20)
                            worksheet.write(row + 3, col + 1,
                                            str(total_remaining_achieved) if total_remaining_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 3, col + 1, 20)

                        else:
                            col = 10
                            worksheet.write(row, col,
                                            str(total_data_center_planned) if total_data_center_planned else '0', f2)
                            worksheet.set_column(row, col, 20)
                            worksheet.write(row, col + 1,
                                            str(total_data_center_achieved) if total_data_center_achieved else '0',
                                            f2)
                            worksheet.set_column(row, col + 1, 20)
                            worksheet.write(row + 1, col,
                                            str(total_major_planned) if total_major_planned else '0',
                                            f2)
                            worksheet.set_column(row + 1, col, 20)
                            worksheet.write(row + 1, col + 1,
                                            str(total_major_achieved) if total_major_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 1, col + 1, 20)
                            worksheet.write(row + 2, col,
                                            str(total_normal_planned) if total_normal_planned else '0',
                                            f2)
                            worksheet.set_column(row + 2, col, 20)
                            worksheet.write(row + 2, col + 1,
                                            str(total_normal_achieved) if total_normal_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 2, col + 1, 20)
                            total_planned = total_data_center_planned + total_major_planned + total_normal_planned
                            total_achieved = total_data_center_achieved + total_major_achieved + total_normal_achieved
                            worksheet.write(row + 3, col,
                                            str(total_planned) if total_planned else '0',
                                            f2)
                            worksheet.set_column(row + 3, col, 20)
                            worksheet.write(row + 3, col + 1,
                                            str(total_achieved) if total_achieved else '0',
                                            f2)
                            worksheet.set_column(row + 3, col + 1, 20)
                            row += 4
                    else:
                        week1_planned = region_generator_planning_lines.filtered(
                            lambda l: 1 <= l.date.day <= 7)
                        week1_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 1 <= l.date.day <= 7 and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week2_planned = region_generator_planning_lines.filtered(
                            lambda l: 8 <= l.date.day <= 15)
                        week2_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 8 <= l.date.day <= 15 and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week3_planned = region_generator_planning_lines.filtered(
                            lambda l: 16 <= l.date.day <= 21)
                        week3_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 16 <= l.date.day <= 21 and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)
                        week4_planned = region_generator_planning_lines.filtered(
                            lambda l: 22 <= l.date.day <= 28)
                        week4_achieved = region_generator_planning_lines.filtered(
                            lambda
                                l: 22 <= l.date.day <= 28 and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)

                        region_range = 'A' + str(row + 1) + ':B' + str(row + 1)
                        worksheet.merge_range(region_range, region_obj.name, f2)
                        worksheet.set_column(region_range, 20)
                        col += 1

                        worksheet.write(row, col, str(len(week1_planned)) if week1_planned else '0',
                                        f2)
                        worksheet.set_column(row, col, 20)
                        worksheet.write(row, col + 1,
                                        str(len(week1_achieved)) if week1_achieved else '0', f2)
                        worksheet.set_column(row, col + 1, 20)
                        worksheet.write(row, col + 2,
                                        str(len(week2_planned)) if week2_planned else '0', f2)
                        worksheet.set_column(row, col + 2, 20)
                        worksheet.write(row, col + 3,
                                        str(len(week2_achieved)) if week2_achieved else '0', f2)
                        worksheet.set_column(row, col + 3, 20)
                        worksheet.write(row, col + 4,
                                        str(len(week3_planned)) if week3_planned else '0', f2)
                        worksheet.set_column(row, col + 4, 20)
                        worksheet.write(row, col + 5,
                                        str(len(week3_achieved)) if week3_achieved else '0', f2)
                        worksheet.set_column(row, col + 5, 20)
                        worksheet.write(row, col + 6,
                                        str(len(week4_planned)) if week4_planned else '0', f2)
                        worksheet.set_column(row, col + 6, 20)
                        worksheet.write(row, col + 7,
                                        str(len(week4_achieved)) if week4_achieved else '0', f2)
                        worksheet.set_column(row, col + 7, 20)
                        if remaining:
                            remaining_planned = region_generator_planning_lines.filtered(
                                lambda l: 29 <= l.date.day <= month_days)
                            remaining_achieved = region_generator_planning_lines.filtered(
                                lambda
                                    l: 29 <= l.date.day <= month_days and l.maintenance_request_id and l.maintenance_request_id.timer_first_start)

                            # Remaining
                            worksheet.write(row, col + 8, str(len(
                                remaining_planned)) if remaining_planned else '0', f2)
                            worksheet.set_column(row, col + 8, 20)
                            worksheet.write(row, col + 9,
                                            str(len(
                                                remaining_achieved)) if remaining_achieved else '0',
                                            f2)
                            worksheet.set_column(row, col + 9, 20)
                            # Total Of Total
                            total_planned_remaining = len(week1_planned) + len(week2_planned) + len(
                                week3_planned) + len(
                                week4_planned) + len(remaining_planned)
                            total_achieved_remaining = len(week1_achieved) + len(week2_achieved) + len(
                                week3_achieved) + len(week4_achieved) + len(remaining_achieved)

                            worksheet.write(row, col + 10,
                                            str(total_planned_remaining) if total_planned_remaining else '0', f2)
                            worksheet.set_column(row, col + 10, 20)
                            worksheet.write(row, col + 11,
                                            str(total_achieved_remaining) if total_achieved_remaining else '0',
                                            f2)
                            worksheet.set_column(row, col + 11, 20)
                        else:
                            # Total Of Total
                            total_planned_remaining = len(week1_planned) + len(week2_planned) + len(
                                week3_planned) + len(
                                week4_planned)
                            total_achieved_remaining = len(week1_achieved) + len(week2_achieved) + len(
                                week3_achieved) + len(week4_achieved)

                            worksheet.write(row, col + 8,
                                            str(total_planned_remaining) if total_planned_remaining else '0', f2)
                            worksheet.set_column(row, col + 8, 20)
                            worksheet.write(row, col + 9,
                                            str(total_achieved_remaining) if total_achieved_remaining else '0',
                                            f2)
                            worksheet.set_column(row, col + 9, 20)
                        row += 1
        else:
            worksheet.merge_range('A7:B8', 'PPM Monthly Report #' + str(month), f11)
            activity_row = 0
            activity_col = 4
            for activity in self.env['maintenance.request.activity'].sudo().search([]):
                worksheet.write(activity_row, activity_col, str(activity.code), f55)
                worksheet.write(activity_row, activity_col + 1, str(activity.name), f55)
                activity_row += 1
            # PPM Monthly Activity Report
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            maintenance_requests = self.env['maintenance.request'].sudo().search(
                [('request_date', '>=', start_date), ('request_date', '<=', end_date),
                 ('maintenance_tag', '=', 'generators')])
            sites = []
            generator_rhs = []
            generators = []
            for maintenance_request in maintenance_requests:
                if maintenance_request.equipment_id and maintenance_request.equipment_id.id not in sites:
                    sites.append(maintenance_request.equipment_id.id)
                if maintenance_request.generator_rh_ids:
                    for g_rh in maintenance_request.generator_rh_ids:
                        if g_rh.id not in generator_rhs:
                            generator_rhs.append(g_rh.id)
                        if g_rh.generator_id.id not in generators:
                            generators.append(g_rh.generator_id.id)
            activity_row += 1
            worksheet.write(activity_row + 1, 0, '#', f4)
            worksheet.write(activity_row + 1, 1, 'Site Code', f4)
            worksheet.set_column(activity_row + 1, 1, 20)
            worksheet.write(activity_row + 1, 2, 'Site Type', f4)
            worksheet.set_column(activity_row + 1, 2, 20)
            worksheet.write(activity_row + 1, 3, 'Site Category', f4)
            worksheet.set_column(activity_row + 1, 3, 20)
            worksheet.write(activity_row + 1, 4, 'Site Status', f4)
            worksheet.set_column(activity_row + 1, 4, 20)
            worksheet.write(activity_row + 1, 5, 'No of generators', f4)
            worksheet.set_column(activity_row + 1, 5, 20)
            worksheet.write(activity_row + 1, 6, '1st M Plan', f4)
            worksheet.set_column(activity_row + 1, 6, 20)
            worksheet.write(activity_row + 1, 7, '1st M Actual', f4)
            worksheet.set_column(activity_row + 1, 7, 20)
            worksheet.write(activity_row + 1, 8, 'G1RH', f4)
            worksheet.set_column(activity_row + 1, 8, 20)
            worksheet.write(activity_row + 1, 9, 'G2RH', f4)
            worksheet.set_column(activity_row + 1, 9, 20)
            g_col = 10
            worksheet.write(activity_row + 1, g_col, 'Status', f4)
            worksheet.set_column(activity_row + 1, g_col, 20)
            worksheet.write(activity_row + 1, g_col + 1, 'Activity', f4)
            worksheet.set_column(activity_row + 1, g_col + 1, 20)
            worksheet.write(activity_row + 1, g_col + 2, 'Remark', f4)
            worksheet.set_column(activity_row + 1, g_col + 2, 20)
            worksheet.write(activity_row + 1, g_col + 3, '2nd M Plan', f4)
            worksheet.set_column(activity_row + 1, g_col + 3, 20)
            worksheet.write(activity_row + 1, g_col + 4, '2nd M Actual', f4)
            worksheet.set_column(activity_row + 1, g_col + 4, 20)
            worksheet.write(activity_row + 1, g_col + 5, 'G1RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 5, 20)
            worksheet.write(activity_row + 1, g_col + 6, 'G2RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 6, 20)
            worksheet.write(activity_row + 1, g_col + 7, 'Status', f4)
            worksheet.set_column(activity_row + 1, g_col + 7, 20)
            worksheet.write(activity_row + 1, g_col + 8, 'Activity', f4)
            worksheet.set_column(activity_row + 1, g_col + 8, 20)
            worksheet.write(activity_row + 1, g_col + 9, 'Remark', f4)
            worksheet.set_column(activity_row + 1, g_col + 9, 20)
            worksheet.write(activity_row + 1, g_col + 10, '3rd M Plan', f4)
            worksheet.set_column(activity_row + 1, g_col + 10, 20)
            worksheet.write(activity_row + 1, g_col + 11, '3rd M Actual', f4)
            worksheet.set_column(activity_row + 1, g_col + 11, 20)
            worksheet.write(activity_row + 1, g_col + 12, 'G1RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 12, 20)
            worksheet.write(activity_row + 1, g_col + 13, 'G2RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 13, 20)
            worksheet.write(activity_row + 1, g_col + 14, 'Status', f4)
            worksheet.set_column(activity_row + 1, g_col + 14, 20)
            worksheet.write(activity_row + 1, g_col + 15, 'Activity', f4)
            worksheet.set_column(activity_row + 1, g_col + 15, 20)
            worksheet.write(activity_row + 1, g_col + 16, 'Remark', f4)
            worksheet.set_column(activity_row + 1, g_col + 16, 20)
            worksheet.write(activity_row + 1, g_col + 17, '4th M Plan', f4)
            worksheet.set_column(activity_row + 1, g_col + 17, 20)
            worksheet.write(activity_row + 1, g_col + 18, '4th M Actual', f4)
            worksheet.set_column(activity_row + 1, g_col + 18, 20)
            worksheet.write(activity_row + 1, g_col + 19, 'G1RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 19, 20)
            worksheet.write(activity_row + 1, g_col + 20, 'G2RH', f4)
            worksheet.set_column(activity_row + 1, g_col + 20, 20)
            worksheet.write(activity_row + 1, g_col + 21, 'Status', f4)
            worksheet.set_column(activity_row + 1, g_col + 21, 20)
            worksheet.write(activity_row + 1, g_col + 22, 'Activity', f4)
            worksheet.set_column(activity_row + 1, g_col + 22, 20)
            worksheet.write(activity_row + 1, g_col + 23, 'Remark', f4)
            worksheet.set_column(activity_row + 1, g_col + 23, 20)
            if sites:
                row = activity_row + 2
                site_no = 1
                for site in sites:
                    site_obj = self.env['maintenance.equipment'].sudo().browse(site)
                    site_generator_planning_lines = self.env['generator.planning.line'].sudo().search(
                        [('date', '>=', start_date), ('date', '<=', end_date), ('site_id', '=', site)],
                        order='date asc')
                    if site_generator_planning_lines:
                        first_generator_planning_lines = site_generator_planning_lines[0]
                    else:
                        first_generator_planning_lines = False

                    worksheet.write(row, 0, str(site_no), f4)
                    worksheet.write(row, 1, str(site_obj.site) if site_obj.site else '', f5)
                    worksheet.set_column(row, 1, 20)
                    worksheet.write(row, 2, str(site_obj.site_type_id.name) if site_obj.site_type_id else '', f5)
                    worksheet.set_column(row, 2, 20)
                    worksheet.write(row, 3, str(site_obj.category_id.name) if site_obj.category_id else '', f5)
                    worksheet.set_column(row, 3, 20)
                    worksheet.write(row, 4, 'Active', f5)
                    worksheet.set_column(row, 4, 20)
                    worksheet.write(row, 5, str(len(site_obj.generator_ids) if site_obj.generator_ids else 0), f5)
                    worksheet.set_column(row, 5, 20)
                    worksheet.write(row, 6,
                                    str(first_generator_planning_lines.date) if first_generator_planning_lines and first_generator_planning_lines.date else '',
                                    f6)
                    worksheet.set_column(row, 6, 20)
                    worksheet.write(row, 7,
                                    str(first_generator_planning_lines.maintenance_request_id.timer_first_start) if first_generator_planning_lines and first_generator_planning_lines.maintenance_request_id and first_generator_planning_lines.maintenance_request_id.timer_first_start else '',
                                    f6)
                    worksheet.set_column(row, 7, 20)

                    if first_generator_planning_lines and first_generator_planning_lines.maintenance_request_id and first_generator_planning_lines.maintenance_request_id.timer_first_start:
                        g1_rh = first_generator_planning_lines.maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G1')
                        g2_rh = first_generator_planning_lines.maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G2')
                        worksheet.write(row, 8, g1_rh.rh if g1_rh else '', f6)
                        worksheet.set_column(row, 8, 20)
                        worksheet.write(row, 9, g2_rh.rh if g2_rh else '', f6)
                        worksheet.set_column(row, 9, 20)
                    g_column = 10
                    worksheet.write(row, g_column, 'Active', f6)
                    worksheet.set_column(row, g_column, 20)
                    activity_str = ''
                    if first_generator_planning_lines and first_generator_planning_lines.maintenance_request_id and first_generator_planning_lines.maintenance_request_id.activity:
                        for activity in first_generator_planning_lines.maintenance_request_id.activity:
                            activity_str += activity.code + ','
                    worksheet.write(row, g_column + 1, str(activity_str), f6)
                    worksheet.set_column(row, g_column + 1, 20)
                    worksheet.write(row, g_column + 2,
                                    str(first_generator_planning_lines.maintenance_request_id.remark) if first_generator_planning_lines and first_generator_planning_lines.maintenance_request_id and first_generator_planning_lines.maintenance_request_id.remark else '',
                                    f6)
                    worksheet.set_column(row, g_column + 2, 20)
                    # first plan
                    worksheet.write(row, g_column + 3,
                                    str(site_generator_planning_lines[1].date) if site_generator_planning_lines and len(
                                        site_generator_planning_lines) > 1 else '', f6)
                    worksheet.set_column(row, g_column + 3, 20)
                    worksheet.write(row, g_column + 4, str(site_generator_planning_lines[
                                                               1].maintenance_request_id.timer_first_start) if site_generator_planning_lines and len(
                        site_generator_planning_lines) > 1 and site_generator_planning_lines[
                                                                                                                   1].maintenance_request_id and
                                                                                                               site_generator_planning_lines[
                                                                                                                   1].maintenance_request_id.timer_first_start else '',
                                    f6)
                    worksheet.set_column(row, g_column + 4, 20)

                    if site_generator_planning_lines and len(site_generator_planning_lines) > 1 and \
                            site_generator_planning_lines[
                                1] and site_generator_planning_lines[1].maintenance_request_id.timer_first_start:
                        g1_rh = site_generator_planning_lines[1].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G1')
                        g2_rh = site_generator_planning_lines[1].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G2')
                        worksheet.write(row, g_column + 5, g1_rh.rh if g1_rh else '', f6)
                        worksheet.set_column(row, g_column + 5, 20)
                        worksheet.write(row, g_column + 6, g2_rh.rh if g2_rh else '', f6)
                        worksheet.set_column(row, g_column + 6, 20)
                        worksheet.write(row, g_column + 7, 'Active', f6)
                        worksheet.set_column(row, g_column + 7, 20)
                        activity_str = ''
                        if site_generator_planning_lines[1].maintenance_request_id and site_generator_planning_lines[
                            1].maintenance_request_id.activity:
                            for activity in site_generator_planning_lines[1].maintenance_request_id.activity:
                                activity_str += activity.code + ','
                        worksheet.write(row, g_column + 8, str(activity_str), f6)
                        worksheet.set_column(row, g_column + 8, 20)
                        worksheet.write(row, g_column + 9,
                                        str(site_generator_planning_lines[1].maintenance_request_id.remark) if
                                        site_generator_planning_lines[
                                            1] and first_generator_planning_lines.maintenance_request_id and
                                        site_generator_planning_lines[1].maintenance_request_id.remark else '',
                                        f6)
                        worksheet.set_column(row, g_column + 9, 20)
                    else:
                        worksheet.write(row, g_column + 5, '', f6)
                        worksheet.set_column(row, g_column + 5, 20)
                        worksheet.write(row, g_column + 6, '', f6)
                        worksheet.set_column(row, g_column + 6, 20)
                        worksheet.write(row, g_column + 7, '', f6)
                        worksheet.set_column(row, g_column + 7, 20)

                        worksheet.write(row, g_column + 8, '', f6)
                        worksheet.set_column(row, g_column + 8, 20)
                        worksheet.write(row, g_column + 9, '',
                                        f6)
                        worksheet.set_column(row, g_column + 9, 20)

                    # second plan
                    worksheet.write(row, g_column + 10,
                                    str(site_generator_planning_lines[2].date) if site_generator_planning_lines and len(
                                        site_generator_planning_lines) > 2 else '', f6)
                    worksheet.set_column(row, g_column + 10, 20)
                    worksheet.write(row, g_column + 11, str(site_generator_planning_lines[
                                                                2].maintenance_request_id.timer_first_start) if site_generator_planning_lines and len(
                        site_generator_planning_lines) > 2 and site_generator_planning_lines[
                                                                                                                    2].maintenance_request_id and
                                                                                                                site_generator_planning_lines[
                                                                                                                    2].maintenance_request_id.timer_first_start else '',
                                    f6)
                    worksheet.set_column(row, g_column + 11, 20)

                    if site_generator_planning_lines and len(site_generator_planning_lines) > 2 and \
                            site_generator_planning_lines[
                                2] and site_generator_planning_lines[2].maintenance_request_id.timer_first_start:
                        g1_rh = site_generator_planning_lines[2].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G1')
                        g2_rh = site_generator_planning_lines[2].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G2')
                        worksheet.write(row, g_column + 12, g1_rh.rh if g1_rh else '', f6)
                        worksheet.set_column(row, g_column + 12, 20)
                        worksheet.write(row, g_column + 13, g2_rh.rh if g2_rh else '', f6)
                        worksheet.set_column(row, g_column + 13, 20)
                        worksheet.write(row, g_column + 14, 'Active', f6)
                        worksheet.set_column(row, g_column + 14, 20)
                        activity_str = ''
                        if site_generator_planning_lines[2].maintenance_request_id and site_generator_planning_lines[
                            2].maintenance_request_id.activity:
                            for activity in site_generator_planning_lines[2].maintenance_request_id.activity:
                                activity_str += activity.code + ','
                        worksheet.write(row, g_column + 15, str(activity_str), f6)
                        worksheet.set_column(row, g_column + 15, 20)
                        worksheet.write(row, g_column + 16,
                                        str(site_generator_planning_lines[2].maintenance_request_id.remark) if
                                        site_generator_planning_lines[
                                            2] and first_generator_planning_lines.maintenance_request_id and
                                        site_generator_planning_lines[2].maintenance_request_id.remark else '',
                                        f6)
                        worksheet.set_column(row, g_column + 16, 20)
                    else:
                        worksheet.write(row, g_column + 12, '', f6)
                        worksheet.set_column(row, g_column + 12, 20)
                        worksheet.write(row, g_column + 13, '', f6)
                        worksheet.set_column(row, g_column + 13, 20)
                        worksheet.write(row, g_column + 14, '', f6)
                        worksheet.set_column(row, g_column + 14, 20)

                        worksheet.write(row, g_column + 15, '', f6)
                        worksheet.set_column(row, g_column + 15, 20)
                        worksheet.write(row, g_column + 16, '',
                                        f6)
                        worksheet.set_column(row, g_column + 16, 20)

                    # third plan
                    worksheet.write(row, g_column + 17,
                                    str(site_generator_planning_lines[
                                            3].date) if site_generator_planning_lines and len(
                                        site_generator_planning_lines) > 3 else '', f6)
                    worksheet.set_column(row, g_column + 17, 20)
                    worksheet.write(row, g_column + 18, str(site_generator_planning_lines[
                                                                3].maintenance_request_id.timer_first_start) if site_generator_planning_lines and len(
                        site_generator_planning_lines) > 3 and site_generator_planning_lines[
                                                                                                                    3].maintenance_request_id and
                                                                                                                site_generator_planning_lines[
                                                                                                                    3].maintenance_request_id.timer_first_start else '',
                                    f6)
                    worksheet.set_column(row, g_column + 18, 20)

                    if site_generator_planning_lines and len(site_generator_planning_lines) > 3 and \
                            site_generator_planning_lines[
                                3] and site_generator_planning_lines[3].maintenance_request_id.timer_first_start:
                        g1_rh = site_generator_planning_lines[3].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G1')
                        g2_rh = site_generator_planning_lines[3].maintenance_request_id.generator_rh_ids.filtered(
                            lambda gg: gg.generator_id.name == 'G2')
                        worksheet.write(row, g_column + 19, g1_rh.rh if g1_rh else '', f6)
                        worksheet.set_column(row, g_column + 19, 20)
                        worksheet.write(row, g_column + 20, g2_rh.rh if g2_rh else '', f6)
                        worksheet.set_column(row, g_column + 20, 20)
                        worksheet.write(row, g_column + 21, 'Active', f6)
                        worksheet.set_column(row, g_column + 21, 20)
                        activity_str = ''
                        if site_generator_planning_lines[3].maintenance_request_id and \
                                site_generator_planning_lines[
                                    3].maintenance_request_id.activity:
                            for activity in site_generator_planning_lines[3].maintenance_request_id.activity:
                                activity_str += activity.code + ','
                        worksheet.write(row, g_column + 22, str(activity_str), f6)
                        worksheet.set_column(row, g_column + 22, 20)
                        worksheet.write(row, g_column + 23,
                                        str(site_generator_planning_lines[3].maintenance_request_id.remark) if
                                        site_generator_planning_lines[
                                            3] and first_generator_planning_lines.maintenance_request_id and
                                        site_generator_planning_lines[3].maintenance_request_id.remark else '',
                                        f6)
                        worksheet.set_column(row, g_column + 23, 20)
                    else:
                        worksheet.write(row, g_column + 19, '', f6)
                        worksheet.set_column(row, g_column + 19, 20)
                        worksheet.write(row, g_column + 20, '', f6)
                        worksheet.set_column(row, g_column + 20, 20)
                        worksheet.write(row, g_column + 21, '', f6)
                        worksheet.set_column(row, g_column + 21, 20)

                        worksheet.write(row, g_column + 22, '', f6)
                        worksheet.set_column(row, g_column + 22, 20)
                        worksheet.write(row, g_column + 23, '',
                                        f6)
                        worksheet.set_column(row, g_column + 23, 20)

                    row += 1

import base64
import io
from odoo import models


class SitePmReportsXlsx(models.AbstractModel):
    _name = 'report.ejaf_maintenance_planning_reports.site_pm_reports'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_data):
        worksheet = workbook.add_worksheet("Site PM Tracker Report")
        f1 = workbook.add_format(
            {'bold': True, 'font_color': '#000000', 'align': 'center', 'bg_color': '#7dabbd', 'font_size': 16})
        f2 = workbook.add_format(
            {'bold': True, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#a21b0d', 'border': True})
        f3 = workbook.add_format(
            {'bold': True, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#030a6a', 'border': True})
        f4 = workbook.add_format(
            {'bold': False, 'font_color': '#000000', 'align': 'center', 'border': True})
        buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        image_width = 340.0
        image_height = 140.0

        cell_width = 64.0
        cell_height = 20.0

        x_scale = cell_width / image_width
        y_scale = cell_height / image_height

        worksheet.insert_image('A1:B3', "any_name.png",
                               {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
        date_from = data['date_from']
        date_to = data['date_to']
        worksheet.merge_range('A4:B5', 'Site PM Tracker', f1)
        worksheet.set_column('A4:B5', 20)
        maintenance_requests = self.env['maintenance.request'].sudo().search(
            [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'full_site'),
             ('request_date', '>=', date_from), ('request_date', '<=', date_to)])
        no_maintenance_reqs = len(maintenance_requests)
        worksheet.write(5, 0, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 0, 20)
        worksheet.write(5, 1, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 1, 20)
        worksheet.write(5, 2, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 2, 20)
        worksheet.write(5, 3, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 3, 20)
        worksheet.write(5, 4, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 4, 20)
        worksheet.write(5, 5, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 5, 20)
        worksheet.write(5, 6, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 6, 20)
        worksheet.write(5, 7, str(no_maintenance_reqs), f2)
        worksheet.set_column(5, 7, 20)
        worksheet.write(6, 0, '#', f3)
        worksheet.write(6, 1, 'Site Code', f3)
        worksheet.set_column(6, 1, 20)
        worksheet.write(6, 2, 'Site Name', f3)
        worksheet.set_column(6, 2, 20)
        worksheet.write(6, 3, 'Region', f3)
        worksheet.set_column(6, 3, 20)
        worksheet.write(6, 4, 'PM Status 1st Visit', f3)
        worksheet.set_column(6, 4, 20)
        worksheet.write(6, 5, 'Date', f3)
        worksheet.set_column(6, 5, 20)
        worksheet.write(6, 6, 'PM Status 2nd Visit', f3)
        worksheet.set_column(6, 6, 20)
        worksheet.write(6, 7, 'Date', f3)
        worksheet.set_column(6, 7, 10)
        worksheet.write(6, 8, 'Site/Tower needs to ground system', f3)
        worksheet.set_column(6, 8, 150)
        worksheet.write(6, 9, 'Site gate missing or needs repairing', f3)
        worksheet.set_column(6, 9, 150)
        worksheet.write(6, 10, 'Aviation light system missing or not working', f3)
        worksheet.set_column(6, 10, 50)
        worksheet.write(6, 11, 'Base of tower, concrete element not ok', f3)
        worksheet.set_column(6, 11, 50)
        worksheet.write(6, 12, 'commercial power board missing not NOK', f3)
        worksheet.set_column(6, 12, 50)
        worksheet.write(6, 13, 'FM 200 is empty', f3)
        worksheet.set_column(6, 13, 20)
        worksheet.write(6, 14, 'TRSM Status', f3)
        worksheet.set_column(6, 14, 20)
        worksheet.write(6, 15, 'RAUS & RF & RRU & TMA missing ground', f3)
        worksheet.set_column(6, 15, 50)
        row = 7
        count = 1
        first_count = 0
        second_count = 0
        third_count = 0
        forth_count = 0
        fifth_count = 0
        sixth_count = 0
        seventh_count = 0
        eighth_count = 0
        for maintenance_request in maintenance_requests:
            worksheet.write(row, 0, str(count), f3)
            worksheet.set_column(row, 0, 20)
            worksheet.write(row, 1,
                            str(maintenance_request.equipment_id.site) if maintenance_request and maintenance_request.equipment_id and maintenance_request.equipment_id.site else '',
                            f4)
            worksheet.set_column(row, 1, 20)
            worksheet.write(row, 2,
                            str(maintenance_request.equipment_id.name) if maintenance_request and maintenance_request.equipment_id and maintenance_request.equipment_id.name else '',
                            f4)
            worksheet.set_column(row, 2, 20)
            worksheet.write(row, 3,
                            str(maintenance_request.equipment_id.region_id.name) if maintenance_request and maintenance_request.equipment_id and maintenance_request.equipment_id.region_id else '',
                            f4)
            worksheet.set_column(row, 3, 20)
            worksheet.write(row, 4,
                            str(maintenance_request.pm_status_first_visit) if maintenance_request and maintenance_request.pm_status_first_visit else '',
                            f4)
            worksheet.set_column(row, 4, 20)
            worksheet.write(row, 5,
                            str(maintenance_request.pm_status_first_visit_date) if maintenance_request and maintenance_request.pm_status_first_visit_date else '',
                            f4)
            worksheet.set_column(row, 5, 20)
            worksheet.write(row, 6,
                            str(maintenance_request.pm_status_second_visit) if maintenance_request and maintenance_request.pm_status_second_visit else '',
                            f4)
            worksheet.set_column(row, 6, 20)
            worksheet.write(row, 7,
                            str(maintenance_request.pm_status_second_visit_date) if maintenance_request and maintenance_request.pm_status_second_visit_date else '',
                            f4)
            worksheet.set_column(row, 7, 20)
            if maintenance_request.maintenance_team_id:
                technical_questions = self.env['technical.inspection'].search(
                    [('maintenance_id', '=', maintenance_request.id),
                     ('equipment_id', '=', maintenance_request.equipment_id.id)])
                first_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'a')
                first_count += 1 if first_checklist else 0
                second_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'b')
                second_count += 1 if second_checklist else 0
                third_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'c')
                third_count += 1 if third_checklist else 0
                forth_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'd')
                forth_count += 1 if forth_checklist else 0
                fifth_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'e')
                fifth_count += 1 if fifth_checklist else 0
                sixth_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'f')
                sixth_count += 1 if sixth_checklist else 0
                seventh_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'i')
                seventh_count += 1 if seventh_checklist else 0
                eighth_checklist = technical_questions.mapped('question_line_ids').filtered(
                    lambda l: l.question_type == 'j')
                eighth_count += 1 if eighth_checklist else 0
                first_answer = ''
                if first_checklist and first_checklist[0].yes_answer:
                    first_answer = 'Active'
                elif first_checklist and first_checklist[0].no_answer and \
                        first_checklist[0].comment:
                    first_answer = 'No /' + str(first_checklist[0].comment)
                worksheet.write(row, 8, first_answer, f4)
                worksheet.set_column(row, 8, 150)
                second_answer = ''
                if second_checklist and second_checklist[0].yes_answer:
                    second_answer = 'Active'
                elif second_checklist and second_checklist[0].no_answer and second_checklist[0].comment:
                    second_answer = 'No /' + str(second_checklist[0].comment)

                worksheet.write(row, 9, second_answer, f4)
                worksheet.set_column(row, 9, 150)

                third_answer = ''
                if third_checklist and third_checklist[0].yes_answer:
                    third_answer = 'Active'
                elif third_checklist and third_checklist[0].no_answer and third_checklist[0].comment:
                    third_answer = 'No /' + str(third_checklist[0].comment)

                worksheet.write(row, 10, third_answer, f4)
                worksheet.set_column(row, 10, 20)

                forth_answer = ''
                if forth_checklist and forth_checklist[0].yes_answer:
                    forth_answer = 'Active'
                elif forth_checklist and forth_checklist[0].no_answer and forth_checklist[0].comment:
                    forth_answer = 'No /' + str(forth_checklist[0].comment)

                worksheet.write(row, 11, forth_answer, f4)
                worksheet.set_column(row, 11, 20)
                fifth_answer = ''
                if fifth_checklist and fifth_checklist[0].yes_answer:
                    fifth_answer = 'Active'
                elif fifth_checklist and fifth_checklist[0].no_answer and fifth_checklist[0].comment:
                    fifth_answer = 'No /' + str(fifth_checklist[0].comment)

                worksheet.write(row, 12, fifth_answer, f4)
                worksheet.set_column(row, 12, 20)

                sixth_answer = ''
                if sixth_checklist and sixth_checklist[0].yes_answer:
                    sixth_answer = 'Active'
                elif sixth_checklist and sixth_checklist[0].no_answer and sixth_checklist[0].comment:
                    sixth_answer = 'No /' + str(sixth_checklist[0].comment)

                worksheet.write(row, 13, sixth_answer, f4)
                worksheet.set_column(row, 13, 20)
                seventh_answer = ''
                if seventh_checklist and seventh_checklist[0].yes_answer:
                    seventh_answer = 'Active'
                elif seventh_checklist and seventh_checklist[0].no_answer and \
                        seventh_checklist[
                            0].comment:
                    seventh_answer = 'No /' + str(seventh_checklist[0].comment)

                worksheet.write(row, 14, seventh_answer, f4)
                worksheet.set_column(row, 14, 20)
                eighth_answer = ''
                if eighth_checklist and eighth_checklist[0].yes_answer :
                    eighth_answer = 'Active'
                elif eighth_checklist and eighth_checklist[0].no_answer  and \
                        eighth_checklist[0].comment:
                    eighth_answer = 'No /' + str(eighth_checklist[0].comment)

                worksheet.write(row, 15, eighth_answer, f4)
                worksheet.set_column(row, 15, 20)

            row += 1
            count += 1
        worksheet.write(5, 8, str(first_count), f2)
        worksheet.write(5, 9, str(second_count), f2)
        worksheet.write(5, 10, str(third_count), f2)
        worksheet.write(5, 11, str(forth_count), f2)
        worksheet.write(5, 12, str(fifth_count), f2)
        worksheet.write(5, 13, str(sixth_count), f2)
        worksheet.write(5, 14, str(seventh_count), f2)
        worksheet.write(5, 15, str(eighth_count), f2)

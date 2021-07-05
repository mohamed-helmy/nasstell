from odoo import models


class TechnicalInspectionReportXlsx(models.AbstractModel):
    _name = 'report.ejaf_tec_inspection_report.technical_inspection_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet('sheet')

        header_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',
            'font_size': 14,
            'border': 1,
            'bold': 1,

        })

        right_format = workbook.add_format({
            'align': 'right',
            'valign': 'vright',
            'color': 'black',
            'font_size': 9,
            'border': 1,
            'bold': 1,

        })
        left_format = workbook.add_format({
            'align': 'left',
            'valign': 'vleft',
            'color': 'black',
            'font_size': 11,
            'border': 1,
            'bold': 1,

        })
        center_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',
            'font_size': 11,
            'border': 1,

        })
        center_format2 = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',
            'font_size': 11,
            'border': 1,
            'bold': 1,

        })

        header_format3 = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',
            'font_size': 15,
            'border': 1,
            'bold': 1,

        })
        sheet.set_row(10, 25)
        sheet.set_column('A:G', 18)

        # Header of Report data ,titles

        sheet.merge_range("C2:E3", objects.name or "", header_format)

        sheet.write("A5", "Maintenance:", left_format)
        sheet.write("A6", "Start Date:", left_format)
        sheet.write("A7", "Time In:", left_format)
        sheet.write("A8", "Contact:", left_format)
        sheet.write("E5", "Equipment:", left_format)
        sheet.write("E6", "Finish Date:", left_format)
        sheet.write("E7", "Time Out:", left_format)
        sheet.write("B5", objects.maintenance_id.display_name or "", center_format)
        sheet.write("B6", str(objects.start_date) or "", center_format)
        sheet.write("B7", str(objects.time_in) or "", center_format)
        sheet.write("B8", str(objects.contact) or "", center_format)
        sheet.write("F5", objects.equipment_id.display_name or "", center_format)
        sheet.write("F6", str(objects.finish_date) or "", center_format)
        sheet.write("F7", str(objects.time_out) or "", center_format)

        # table Header

        sheet.write("A11", "Checklist Question", center_format2)
        sheet.write("B11", "Yes", center_format2)
        sheet.write("C11", "NO", center_format2)
        sheet.write("D11", "NOT OK", center_format2)
        sheet.write("E11", "NA", center_format2)
        sheet.write("F11", "Comment", center_format2)

        row = 11
        col = 0
        for line in objects.question_line_ids:
            sheet.write(row, col, line.checklist_question_id.display_name or "", center_format)
            sheet.write(row, col + 1, str(line.yes_answer) or "X", center_format)

            sheet.write(row, col + 2, str(line.no_answer) or 'X' or "", center_format)
            sheet.write(row, col + 3, str(line.no_ok_answer) or "X", center_format)
            sheet.write(row, col + 4, str(line.na_answer) or "X", center_format)

            sheet.write(row, col + 5, line.comment or "", center_format)

            row += 1

from odoo import models


class DailyOutageReportXlsx(models.AbstractModel):
    _name = 'report.ejaf_maintenance_planning_reports.daily_outage_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_data):
        worksheet = workbook.add_worksheet("Daily Outage Report")
        f2 = workbook.add_format(
            {'bold': False, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#0d1c7a', 'border': True})
        f22 = workbook.add_format(
            {'bold': False, 'font_color': '#000000', 'align': 'center', 'bg_color': '#ffffff', 'border': True})
        from_date = data['from_date']
        to_date = data['to_date']
        worksheet.write(1, 0, 'NE Type', f2)
        worksheet.set_column(1, 0, 20)
        worksheet.write(1, 1, 'NE Impacted', f2)
        worksheet.set_column(1, 1, 20)
        worksheet.write(1, 2, 'Site ID', f2)
        worksheet.set_column(1, 2, 20)
        worksheet.write(1, 3, 'Gov', f2)
        worksheet.set_column(1, 3, 20)
        worksheet.write(1, 4, 'Effected TRXs', f2)
        worksheet.set_column(1, 4, 20)
        worksheet.write(1, 5, 'Effected Cells', f2)
        worksheet.set_column(1, 5, 20)
        worksheet.write(1, 6, 'Effected Sites', f2)
        worksheet.set_column(1, 6, 20)
        worksheet.write(1, 7, 'BSC Name', f2)
        worksheet.set_column(1, 7, 20)
        worksheet.write(1, 8, 'TG No', f2)
        worksheet.set_column(1, 8, 20)
        worksheet.write(1, 9, 'TT Issuer', f2)
        worksheet.set_column(1, 9, 20)
        worksheet.write(1, 10, 'TT No', f2)
        worksheet.set_column(1, 10, 20)
        worksheet.write(1, 11, 'TT Status', f2)
        worksheet.set_column(1, 11, 20)
        worksheet.write(1, 12, 'Alarm Time', f2)
        worksheet.set_column(1, 12, 20)
        worksheet.write(1, 13, 'TT Issuing Time', f2)
        worksheet.set_column(1, 13, 20)
        worksheet.write(1, 14, 'Restoration Time', f2)
        worksheet.set_column(1, 14, 20)
        worksheet.write(1, 15, 'Outage Duration', f2)
        worksheet.set_column(1, 15, 20)
        worksheet.write(1, 16, 'Alarm Description', f2)
        worksheet.set_column(1, 16, 20)
        worksheet.write(1, 17, 'VOl', f2)
        worksheet.set_column(1, 17, 20)
        worksheet.write(1, 18, 'In-Vol', f2)
        worksheet.set_column(1, 18, 20)
        worksheet.write(1, 19, 'Site Name', f2)
        worksheet.set_column(1, 19, 20)
        worksheet.write(1, 20, 'Outage Category', f2)
        worksheet.set_column(1, 20, 20)
        worksheet.write(1, 21, 'Problem Category', f2)
        worksheet.set_column(1, 21, 20)
        worksheet.write(1, 22, 'Sub Category', f2)
        worksheet.set_column(1, 22, 20)
        worksheet.write(1, 23, 'Root Cause', f2)
        worksheet.set_column(1, 23, 20)
        worksheet.write(1, 24, 'Why it happened?', f2)
        worksheet.set_column(1, 24, 20)
        worksheet.write(1, 25, 'Site Severity', f2)
        worksheet.set_column(1, 25, 20)
        worksheet.write(1, 26, 'Action Taken', f2)
        worksheet.set_column(1, 26, 20)
        worksheet.write(1, 27, 'Any SP used', f2)
        worksheet.set_column(1, 27, 20)
        worksheet.write(1, 28, 'Comment', f2)
        worksheet.set_column(1, 28, 20)
        maintenance_requests = self.env['maintenance.request'].sudo().search(
            [('maintenance_type', 'in', ['emergency', 'corrective']), ('request_date', '>=', from_date),
             ('request_date', '<=', to_date)])
        row = 2
        for maintenance_request in maintenance_requests:
            worksheet.write(row, 0,
                            str(maintenance_request.ne_type_id.name) if maintenance_request and maintenance_request.ne_type_id else '',
                            f22)
            worksheet.set_column(row, 0, 20)
            worksheet.write(row, 1,
                            str(maintenance_request.ne_impacted_id.name) if maintenance_request and maintenance_request.ne_impacted_id else '',
                            f22)
            worksheet.set_column(row, 1, 20)
            worksheet.write(row, 2,
                            str(maintenance_request.site_code) if maintenance_request and maintenance_request.site_code else '',
                            f22)
            worksheet.set_column(row, 2, 20)
            worksheet.write(row, 3,
                            str(maintenance_request.gov.name) if maintenance_request and maintenance_request.gov and maintenance_request.gov.name else '',
                            f22)
            worksheet.set_column(row, 3, 20)
            worksheet.write(row, 4,
                            str(maintenance_request.effected_trxs) if maintenance_request and maintenance_request.effected_trxs else '',
                            f22)
            worksheet.set_column(row, 4, 20)
            worksheet.write(row, 5,
                            str(maintenance_request.effected_cells) if maintenance_request and maintenance_request.effected_cells else '',
                            f22)
            worksheet.set_column(row, 5, 20)
            worksheet.write(row, 6,
                            str(maintenance_request.effected_sites) if maintenance_request and maintenance_request.effected_sites else '',
                            f22)
            worksheet.set_column(row, 6, 20)
            worksheet.write(row, 7,
                            str(maintenance_request.bsc_name) if maintenance_request and maintenance_request.bsc_name else '',
                            f22)
            worksheet.set_column(row, 7, 20)
            worksheet.write(row, 8,
                            str(maintenance_request.tg_number) if maintenance_request and maintenance_request.tg_number else '',
                            f22)
            worksheet.set_column(row, 8, 20)
            worksheet.write(row, 9,
                            str(maintenance_request.tt_issuer) if maintenance_request and maintenance_request.tt_issuer else '',
                            f22)
            worksheet.set_column(row, 9, 20)
            worksheet.write(row, 10,
                            str(maintenance_request.tt_no) if maintenance_request and maintenance_request.tt_no else '',
                            f22)
            worksheet.set_column(row, 10, 20)
            worksheet.write(row, 11,
                            str(maintenance_request.tt_status) if maintenance_request and maintenance_request.tt_status else '',
                            f22)
            worksheet.set_column(row, 11, 20)
            worksheet.write(row, 12,
                            str(maintenance_request.alarm_time) if maintenance_request and maintenance_request.alarm_time else '',
                            f22)
            worksheet.set_column(row, 12, 20)
            worksheet.write(row, 13,
                            str(maintenance_request.tt_issuing_time) if maintenance_request and maintenance_request.tt_issuing_time else '',
                            f22)
            worksheet.set_column(row, 13, 20)
            worksheet.write(row, 14,
                            str(maintenance_request.closing_outage_time) if maintenance_request and maintenance_request.closing_outage_time else '',
                            f22)
            worksheet.set_column(row, 14, 20)
            worksheet.write(row, 15,
                            str(maintenance_request.outage_duration_str) if maintenance_request and maintenance_request.outage_duration_str else '',
                            f22)
            worksheet.set_column(row, 15, 20)
            worksheet.write(row, 16,
                            str(maintenance_request.alarm_description) if maintenance_request and maintenance_request.alarm_description else '',
                            f22)
            worksheet.set_column(row, 16, 20)
            worksheet.write(row, 17,
                            str(maintenance_request.vol_str) if maintenance_request and maintenance_request.vol_str else '',
                            f22)
            worksheet.set_column(row, 17, 20)
            worksheet.write(row, 18,
                            str(maintenance_request.in_vol_str) if maintenance_request and maintenance_request.in_vol_str else '',
                            f22)
            worksheet.set_column(row, 18, 20)
            worksheet.write(row, 19,
                            str(maintenance_request.equipment_id.name) if maintenance_request and maintenance_request.equipment_id else '',
                            f22)
            worksheet.set_column(row, 19, 20)
            worksheet.write(row, 20,
                            str(maintenance_request.outage_category_id.name) if maintenance_request and maintenance_request.outage_category_id else '',
                            f22)
            worksheet.set_column(row, 20, 20)
            worksheet.write(row, 21,
                            str(maintenance_request.problem_category_id.name) if maintenance_request and maintenance_request.problem_category_id else '',
                            f22)
            worksheet.set_column(row, 21, 20)
            worksheet.write(row, 22,
                            str(maintenance_request.sub_category_id.name) if maintenance_request and maintenance_request.sub_category_id else '',
                            f22)
            worksheet.set_column(row, 22, 20)
            worksheet.write(row, 23,
                            str(maintenance_request.route_cause) if maintenance_request and maintenance_request.route_cause else '',
                            f22)
            worksheet.set_column(row, 23, 20)
            worksheet.write(row, 24,
                            str(maintenance_request.why_it_happened) if maintenance_request and maintenance_request.why_it_happened else '',
                            f22)
            worksheet.set_column(row, 24, 20)
            worksheet.write(row, 25,
                            str(maintenance_request.site_severity.name) if maintenance_request and maintenance_request.site_severity else '',
                            f22)
            worksheet.set_column(row, 25, 20)
            worksheet.write(row, 26,
                            str(maintenance_request.action_taken) if maintenance_request and maintenance_request.action_taken else '',
                            f22)
            worksheet.set_column(row, 26, 20)
            worksheet.write(row, 27,
                            str(maintenance_request.any_sp_used) if maintenance_request and maintenance_request.any_sp_used else '',
                            f22)
            worksheet.set_column(row, 27, 20)
            worksheet.write(row, 28,
                            str(maintenance_request.comment) if maintenance_request and maintenance_request.comment else '',
                            f22)
            worksheet.set_column(row, 28, 20)
            row += 1

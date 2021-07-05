from odoo import api, fields, models


class TechnicalInspection(models.Model):
    _inherit = 'technical.inspection'

    def print_xlsx_report(self):
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})

        report = self.env['ir.actions.report']._get_report_from_name(
            'ejaf_tec_inspection_report.technical_inspection_xlsx')

        return {
            'data': data,
            'type': 'ir.actions.report',
            'report_name': report.report_name,
            'report_type': report.report_type,
            'report_file': report.report_file,
        }

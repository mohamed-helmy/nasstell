from odoo import api, fields, models, _


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    category_type = fields.Selection([('hub', 'Hub'), ('mini_hub', 'Mini Hub'), ('normal', 'Normal')], default='normal',
                                     string='Severity Type')

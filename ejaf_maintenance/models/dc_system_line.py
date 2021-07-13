from odoo import api, fields, models


class DcSystemLine(models.Model):
    _name = 'dc.system.line'
    _description = 'Dc System Line'

    rect_brand_id = fields.Many2one(comodel_name="rect.brand", string="Rect Brand", required=False, )
    maintenance_equipment_id = fields.Many2one(comodel_name="maintenance.equipment", string="", required=False, )
    rect_od = fields.Char(string="Rect OD/ID", required=False, )
    rect_psu_qty = fields.Float(string="Rect PSU Qty", required=False, )
    rect_batt_qty = fields.Float(string="Rect Batt/ Qty", required=False, )
    rect_battery_manufacturing = fields.Char(string="Rect Battery Manufacturing Date", required=False, )
    rect_battery_model = fields.Char(string="Rect Battery Model / AH", required=False, )

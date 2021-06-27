from odoo import api, fields, models


class BatteryManufacturer(models.Model):
    _name = 'battery.manufacturer'
    _rec_name = 'name'

    name = fields.Char()

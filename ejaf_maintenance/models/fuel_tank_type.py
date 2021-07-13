from odoo import api, fields, models


class FuelTankType(models.Model):
    _name = 'fuel.tank.type'
    _description = 'Fuel Tank Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

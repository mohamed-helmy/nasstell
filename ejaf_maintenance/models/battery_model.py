from odoo import api, fields, models


class BatteryModel(models.Model):
    _name = 'battery.model'
    _description = 'Battery Model'
    _rec_name = 'name'

    name = fields.Char(string='Name')

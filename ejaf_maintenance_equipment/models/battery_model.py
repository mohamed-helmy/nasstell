from odoo import api, fields, models


class BatteryModel(models.Model):
    _name = 'battery.model'
    _rec_name = 'name'

    name = fields.Char()

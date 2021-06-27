from odoo import api, fields, models


class GenSetManufacturer(models.Model):
    _name = 'gen.set.manufacturer'
    _rec_name = 'name'

    name = fields.Char()

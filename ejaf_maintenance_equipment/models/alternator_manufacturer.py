from odoo import api, fields, models


class AlternatorManufacturer(models.Model):
    _name = 'alternator.manufacturer'
    _rec_name = 'name'

    name = fields.Char()

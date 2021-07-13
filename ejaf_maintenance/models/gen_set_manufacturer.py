from odoo import api, fields, models


class GenSetManufacturer(models.Model):
    _name = 'gen.set.manufacturer'
    _description = 'Gen Set Manufacturer'
    _rec_name = 'name'

    name = fields.Char(string='Name')

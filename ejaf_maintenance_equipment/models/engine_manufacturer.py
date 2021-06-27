from odoo import api, fields, models



class EngineManufacturer(models.Model):
    _name = 'engine.manufacturer'
    _rec_name = 'name'

    name = fields.Char(string='Name')

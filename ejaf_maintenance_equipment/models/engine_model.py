from odoo import api, fields, models



class EngineModel(models.Model):
    _name = 'engine.model'
    _rec_name = 'name'

    name = fields.Char(string='Name')

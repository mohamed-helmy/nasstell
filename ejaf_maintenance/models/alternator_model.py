from odoo import api, fields, models


class AlternatorModel(models.Model):
    _name = 'alternator.model'
    _rec_name = 'name'
    _description = 'Alternator Model'

    name = fields.Char(string='Name')

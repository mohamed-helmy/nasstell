from odoo import api, fields, models, _


class GeneratorAlternator(models.Model):
    _name = 'generator.alternator.type'
    _rec_name = 'name'
    _description = 'Generator Alternator Type'

    name = fields.Char(string='Name', required=True)


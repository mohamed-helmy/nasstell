from odoo import api, fields, models


class RbsModel(models.Model):
    _name = 'rbs.model'
    _description = 'Rbs Model'
    _rec_name = 'name'

    name = fields.Char(string='Name')

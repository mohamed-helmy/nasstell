from odoo import api, fields, models


class LType(models.Model):
    _name = 'l.type'
    _description = 'L Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

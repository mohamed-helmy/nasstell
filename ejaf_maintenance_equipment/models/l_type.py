from odoo import api, fields, models


class LType(models.Model):
    _name = 'l.type'
    _rec_name = 'name'

    name = fields.Char()

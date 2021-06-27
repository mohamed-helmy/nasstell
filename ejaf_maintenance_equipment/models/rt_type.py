from odoo import api, fields, models



class RtType(models.Model):
    _name = 'rt.type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

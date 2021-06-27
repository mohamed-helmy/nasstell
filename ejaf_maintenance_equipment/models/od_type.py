from odoo import api, fields, models



class OdType(models.Model):
    _name = 'od.type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

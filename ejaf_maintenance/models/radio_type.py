from odoo import api, fields, models


class RadioType(models.Model):
    _name = 'radio.type'
    _description = 'Radio Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

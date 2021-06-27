from odoo import api, fields, models


class RectBrand(models.Model):
    _name = 'rect.brand'
    _rec_name = 'name'

    name = fields.Char()

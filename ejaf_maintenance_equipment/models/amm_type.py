from odoo import api, fields, models


class AmmType(models.Model):
    _name = 'amm.type'
    _rec_name = 'name'

    name = fields.Char()

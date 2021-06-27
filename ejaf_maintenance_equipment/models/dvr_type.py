from odoo import api, fields, models


class DvrType(models.Model):
    _name = 'dvr.type'
    _rec_name = 'name'

    name = fields.Char()

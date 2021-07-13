from odoo import api, fields, models, _


class OutageCategory(models.Model):
    _name = 'outage.category'
    _description = 'Outage Category'

    name = fields.Char(required=True, string='Name')

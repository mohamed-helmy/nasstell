from odoo import models, fields, api, exceptions


class OutagType(models.Model):
    _name = 'outage.type'
    _description = 'Outage Type'

    name = fields.Char(required=True, string='Name')

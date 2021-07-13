from odoo import api, fields, models


class CluStatus(models.Model):
    _name = 'clu.status'
    _description = 'Clu Status'
    _rec_name = 'name'

    name = fields.Char(string='Name')

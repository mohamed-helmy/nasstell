from odoo import api, fields, models



class CluStatus(models.Model):
    _name = 'clu.status'
    _rec_name = 'name'

    name = fields.Char()

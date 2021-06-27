from odoo import api, fields, models



class AtsModel(models.Model):
    _name = 'ats.model'
    _rec_name = 'name'

    name = fields.Char(string='Name')

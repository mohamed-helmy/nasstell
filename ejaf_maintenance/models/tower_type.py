from odoo import api, fields, models


class TowerType(models.Model):
    _name = 'tower.type'
    _description = 'Tower Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

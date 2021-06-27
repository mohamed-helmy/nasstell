from odoo import api, fields, models



class TowerType(models.Model):
    _name = 'tower.type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

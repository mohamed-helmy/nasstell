from odoo import api, fields, models


class TowerTopology(models.Model):
    _name = 'tower.topology'
    _description = 'Tower Topology'
    _rec_name = 'name'

    name = fields.Char(string='Name')

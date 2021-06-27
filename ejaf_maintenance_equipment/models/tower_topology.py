from odoo import api, fields, models


class TowerTopology(models.Model):
    _name = 'tower.topology'
    _rec_name = 'name'

    name = fields.Char()

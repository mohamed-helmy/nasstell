from odoo import api, fields, models


class AntennaType(models.Model):
    _name = 'antenna.type'
    _rec_name = 'name'

    name = fields.Char()

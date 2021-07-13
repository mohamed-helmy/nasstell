from odoo import api, fields, models


class AntennaType(models.Model):
    _name = 'antenna.type'
    _description = 'Antenna Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

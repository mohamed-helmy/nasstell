from odoo import api, fields, models


class MmuType(models.Model):
    _name = 'mmu.type'
    _description = 'Mmu Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')

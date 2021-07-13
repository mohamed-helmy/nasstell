# -*- coding: utf-8 -*-
from odoo import api, fields, models


class NeType(models.Model):
    _name = 'ne.type'
    _rec_name = 'name'
    _description = 'Ne Type'

    name = fields.Char(string='Name')

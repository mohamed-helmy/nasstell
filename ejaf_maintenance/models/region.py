# -*- coding: utf-8 -*-
from odoo import api, fields, models



class Region(models.Model):
    _name = 'region'
    _rec_name = 'name'
    _description = 'Region'

    name = fields.Char(string='Name')

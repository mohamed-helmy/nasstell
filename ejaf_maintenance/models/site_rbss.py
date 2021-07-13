# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Siterbss(models.Model):
    _name = 'site.rbss'
    _rec_name = 'name'
    _description = 'Site Rbss'

    name = fields.Char(string='Name', required=True)
    value = fields.Integer()

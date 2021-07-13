# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SiteType(models.Model):
    _name = 'site.type'
    _description = 'Site Type'

    name = fields.Char(string='Type')

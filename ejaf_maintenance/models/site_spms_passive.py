# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SiteSpmsPassive(models.Model):
    _name = 'site.spms.passive'
    _rec_name = 'name'
    _description = 'Site Spms Passive'

    name = fields.Char(string='Name', required=True)

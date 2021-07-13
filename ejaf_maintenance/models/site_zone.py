# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SiteZone(models.Model):
    _name = 'site.zone'
    _rec_name = 'name'
    _description = 'Site Zone'

    name = fields.Char(string='Name', required=True)

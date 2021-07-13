# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SiteSpmsActive(models.Model):
    _name = 'site.spms.active'
    _rec_name = 'name'
    _description = 'Site Spms Active'

    name = fields.Char(string='Name', required=True)

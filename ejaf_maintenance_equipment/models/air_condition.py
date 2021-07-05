# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SiteAirCondition(models.Model):
    _name = 'site.air.condition'
    _rec_name = 'name'
    _description = 'Site Air Condition'

    name = fields.Char(string='Name', required=True)
    site_id = fields.Many2one(comodel_name="maintenance.equipment", required=False, ondelete="cascade")
    site_name = fields.Char(string='Site', related='site_id.name')
    ac_capacity = fields.Float(string="A/C  Capacity (BTU)")
    ac_brand = fields.Char(string="A/C BRAND")

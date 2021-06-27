# -*- coding: utf-8 -*-
from odoo import api, fields, models


class NeImpacted(models.Model):
    _name = 'ne.impacted'
    _rec_name = 'name'
    _description = 'Ne Impacted'

    name = fields.Char(string='Name')

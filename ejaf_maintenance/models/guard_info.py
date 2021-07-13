# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GuardInfo(models.Model):
    _name = 'guard.info'
    _description = 'Guard Info'

    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    salary = fields.Float(string='Salary')
    currency_id = fields.Many2one('res.currency', string='Currency')

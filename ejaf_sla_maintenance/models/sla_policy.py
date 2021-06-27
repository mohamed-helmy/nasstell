# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class SlaPolicy(models.Model):
    _name = 'sla.policy'
    _description = 'Sla Policy'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    sla_policy_line_ids = fields.One2many('sla.policy.line', 'sla_policy_id', string='Lines')


class SlaPolicyLine(models.Model):
    _name = 'sla.policy.line'
    _description = 'Sla Policy Line'

    sla_policy_id = fields.Many2one('sla.policy', string='Sla Policy')
    priority = fields.Selection([('critical', 'Critical'), ('major', 'Major'), ('minor', 'Minor')], default='critical',
                                string='Priority')
    site_category = fields.Selection([('hub', 'Hub'), ('mini_hub', 'Mini Hub'), ('normal', 'Normal')], default='normal',
                                     string='Site Category')

    duration = fields.Char(string='Duration',default='00:00:00')
    deductions = fields.Float(string='Deductions')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

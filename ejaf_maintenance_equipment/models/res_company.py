# -*- coding: utf-8 -*-

from odoo import fields, models


class CompanyInherit(models.Model):
    _inherit = 'res.company'

    site_planning_notify_period = fields.Integer(string='Site Planning Notify Period')
    generator_planning_notify_period = fields.Integer(string='Generator Planning Notify Period')
    fuel_planning_notify_period = fields.Integer(string='Fuel Planning Notify Period')

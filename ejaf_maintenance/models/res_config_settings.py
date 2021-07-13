# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    site_planning_notify_period = fields.Integer(related='company_id.site_planning_notify_period',
                                                 string='Site Planning Notify Period', readonly=False)
    generator_planning_notify_period = fields.Integer(related='company_id.generator_planning_notify_period',
                                                      string='Generator Planning Notify Period', readonly=False)
    fuel_planning_notify_period = fields.Integer(related='company_id.fuel_planning_notify_period',
                                                 string='Fuel Planning Notify Period', readonly=False)
    reservation_liters = fields.Float(string='Reservation Liters', related='company_id.reservation_liters',readonly=False)
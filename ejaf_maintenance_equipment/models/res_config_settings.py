# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    site_planning_notify_period = fields.Integer(related='company_id.site_planning_notify_period',
                                                 string='Site Planning Notify Period', readonly=False)
    generator_planning_notify_period = fields.Integer(related='company_id.generator_planning_notify_period',
                                                      string='Generator Planning Notify Period', readonly=False)
    fuel_planning_notify_period = fields.Integer(related='company_id.fuel_planning_notify_period',
                                                 string='Fuel Planning Notify Period', readonly=False)
    reservation_liters = fields.Integer(string='Reservation Liters')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            reservation_liters=int(params.get_param('reservation_liters'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_parameter = self.env['ir.config_parameter'].sudo()
        ir_parameter.set_param('reservation_liters', self.reservation_liters)

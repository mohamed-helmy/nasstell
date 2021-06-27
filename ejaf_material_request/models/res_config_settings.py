# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    picking_type_id = fields.Many2one('stock.picking.type', string='Transfer Operation')
    return_picking_type_id = fields.Many2one('stock.picking.type', string='Return Operation')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            picking_type_id=int(params.get_param('picking_type_id')),
            return_picking_type_id=int(params.get_param('return_picking_type_id'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_parameter = self.env['ir.config_parameter'].sudo()
        ir_parameter.set_param('picking_type_id', self.picking_type_id.id)
        ir_parameter.set_param('return_picking_type_id', self.return_picking_type_id.id)

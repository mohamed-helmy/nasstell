# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    picking_type_id = fields.Many2one('stock.picking.type', string='Transfer Operation')
    return_picking_type_id = fields.Many2one('stock.picking.type', string='Return Operation')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    picking_type_id = fields.Many2one(related='company_id.picking_type_id', string='Transfer Operation',readonly=False)
    return_picking_type_id = fields.Many2one(related='company_id.return_picking_type_id', string='Return Operation',readonly=False)


# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    _name = 'material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread']

    def _get_picking_type(self):
        picking_type = int(self.env['ir.config_parameter'].sudo().get_param('picking_type_id'))
        return picking_type if picking_type else False

    def _get_return_picking_type(self):
        picking_type = int(self.env['ir.config_parameter'].sudo().get_param('return_picking_type_id'))
        return picking_type if picking_type else False

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request')
    site_id = fields.Many2one('maintenance.equipment', string='Site', related='maintenance_request_id.equipment_id', store=1)
    line_ids = fields.One2many('material.request.line', 'material_request_id', string='Lines')
    picking_id = fields.Many2one('stock.picking', string='Picking')
    state = fields.Selection(
        [('draft', 'Draft'), ('requested', 'Requested'), ('transferred', 'Transferred'), ('received', 'Received')],
        default='draft')
    picking_type_id = fields.Many2one('stock.picking.type', string='Transfer Operation', default=_get_picking_type)
    return_picking_type_id = fields.Many2one('stock.picking.type', string='Transfer Operation',
                                             default=_get_return_picking_type)
    returned = fields.Boolean(string='Returned')

    @api.model
    def create(self, values):
        if not values.get('name'):
            if not values.get('returned'):
                values['name'] = self.env['ir.sequence'].next_by_code('maintenance.material.request')
            else:
                values['name'] = self.env['ir.sequence'].next_by_code('maintenance.material.request.return')
        return super(MaterialRequest, self).create(values)

    def action_receive(self):
        for material in self:
            material.state = 'received'

    def _create_stock_moves(self, move_line_values_list, picking):
        for values in move_line_values_list:
            values['picking_id'] = picking.id
            self.env['stock.move'].create(values)
        return True

    def action_request(self):
        for material in self:
            if not material.line_ids:
                raise ValidationError('Please add lines to request')
            material.state = 'requested'
            if material.returned and not material.return_picking_type_id:
                raise ValidationError("You must define return picking type")
            if not material.returned and not material.picking_type_id:
                raise ValidationError("You must define picking type")
            if not material.returned:
                picking_type = material.picking_type_id
            else:
                picking_type = material.return_picking_type_id
            picking = self.env['stock.picking'].create({'picking_type_id': picking_type.id,
                                                        'location_id': picking_type.default_location_src_id.id,
                                                        'location_dest_id': picking_type.default_location_dest_id.id})
            if material.returned:
                picking.name = 'Returned Of' + str(material.name)
            for line in material.line_ids:
                self.env['stock.move'].sudo().create({
                    'name': material.name,
                    'picking_id': picking.id,
                    'material_id': material.id if material.returned else False,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                    'product_uom': line.uom_id.id,
                    'date': fields.Datetime.now(),
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id
                })
            picking.material_request_id = material.id
            picking.action_confirm()
            material.picking_id = picking.id


class MaterialRequestLine(models.Model):
    _name = 'material.request.line'
    _description = 'Material Request Line'

    material_request_id = fields.Many2one('material.request')
    returned = fields.Boolean(string='Returned', related='material_request_id.returned')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Integer(string='Quantity')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure',
                             domain="[('category_id', '=', product_uom_category_id)]")
    lot_id = fields.Many2one('stock.production.lot', string='Lot')
    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status', default='normal')

    @api.onchange('lot_id')
    def _set_product_status(self):
        for line in self:
            if line.lot_id and line.lot_id.product_status:
                line.product_status = line.lot_id.product_status

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

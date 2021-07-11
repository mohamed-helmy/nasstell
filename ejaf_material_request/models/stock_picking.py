from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_request_id = fields.Many2one('material.request', string='Material Request')
    site_id = fields.Many2one('maintenance.equipment', string='Site')

    def action_assign(self):
        for picking in self:
            res = super(StockPicking, self).action_assign()
            if picking.material_request_id:
                for move in picking.move_ids_without_package:
                    if picking.material_request_id.line_ids:
                        move.move_line_ids = [(2, ll.id) for ll in move.move_line_ids]
                    for line in picking.material_request_id.line_ids:
                        self.env['stock.move.line'].sudo().create({
                            'move_id': move.id,
                            'picking_id': picking.id,
                            'material_line_id': line.id if picking.material_request_id.returned else False,
                            'product_id': line.product_id.id,
                            'lot_id': line.lot_id.id if line.lot_id else False,
                            'product_status': line.product_status if line.product_status else 'normal',
                            'product_uom_qty': line.qty,
                            'product_uom_id': line.uom_id.id,
                            'date': fields.Datetime.now(),
                            'location_id': picking.picking_type_id.default_location_src_id.id,
                            'location_dest_id': picking.site_id.site_location_id.id
                        })

            return res

    def _action_done(self):
        subtype_commit = self.env.ref("mail.mt_comment")
        for picking in self:
            res = super(StockPicking, self)._action_done()
            if picking.material_request_id:
                user = picking.material_request_id.maintenance_request_id.maintenance_team_id.team_leader_id if picking.material_request_id and picking.material_request_id.maintenance_request_id and picking.material_request_id.maintenance_request_id.maintenance_team_id and picking.material_request_id.maintenance_request_id.maintenance_team_id.team_leader_id and picking.material_request_id.maintenance_request_id.maintenance_team_id.team_leader_id.partner_id else False
                if user:
                    partner_ids = [user.partner_id.id]
                    picking.message_post(
                        partner_ids=partner_ids,
                        subject=_('Check the material request [%s] for the maintenance request  %s') % (
                            picking.material_request_id.name, picking.material_request_id.maintenance_request_id.name),
                        message_type='email',
                        subtype_id=subtype_commit.id
                    )
                picking.material_request_id.state = 'transferred'
            return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    material_id = fields.Many2one('material.request')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    material_line_id = fields.Many2one('material.request.line')


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        """ Increase the reserved quantity, i.e. increase `reserved_quantity` for the set of quants
        sharing the combination of `product_id, location_id` if `strict` is set to False or sharing
        the *exact same characteristics* otherwise. Typically, this method is called when reserving
        a move or updating a reserved move line. When reserving a chained move, the strict flag
        should be enabled (to reserve exactly what was brought). When the move is MTS,it could take
        anything from the stock, so we disable the flag. When editing a move line, we naturally
        enable the flag, to reflect the reservation according to the edition.

        :return: a list of tuples (quant, quantity_reserved) showing on which quant the reservation
            was done and how much the system was able to reserve on it
        """
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id,
                              strict=strict)
        reserved_quants = []

        if float_compare(quantity, 0, precision_rounding=rounding) > 0:
            # if we want to reserve
            available_quantity = self._get_available_quantity(product_id, location_id, lot_id=lot_id,
                                                              package_id=package_id, owner_id=owner_id, strict=strict)
            if float_compare(quantity, available_quantity, precision_rounding=rounding) > 0:
                raise UserError(_('It is not possible to reserve more products of %s than you have in stock.',
                                  product_id.display_name))
        elif float_compare(quantity, 0, precision_rounding=rounding) < 0:
            # if we want to unreserve
            available_quantity = sum(quants.mapped('reserved_quantity'))
            # if float_compare(abs(quantity), available_quantity, precision_rounding=rounding) > 0:
            #     raise UserError(_('It is not possible to unreserve more products of %s than you have in stock.',
            #                       product_id.display_name))
        else:
            return reserved_quants

        for quant in quants:
            if float_compare(quantity, 0, precision_rounding=rounding) > 0:
                max_quantity_on_quant = quant.quantity - quant.reserved_quantity
                if float_compare(max_quantity_on_quant, 0, precision_rounding=rounding) <= 0:
                    continue
                max_quantity_on_quant = min(max_quantity_on_quant, quantity)
                quant.reserved_quantity += max_quantity_on_quant
                reserved_quants.append((quant, max_quantity_on_quant))
                quantity -= max_quantity_on_quant
                available_quantity -= max_quantity_on_quant
            else:
                max_quantity_on_quant = min(quant.reserved_quantity, abs(quantity))
                quant.reserved_quantity -= max_quantity_on_quant
                reserved_quants.append((quant, -max_quantity_on_quant))
                quantity += max_quantity_on_quant
                available_quantity += max_quantity_on_quant

            if float_is_zero(quantity, precision_rounding=rounding) or float_is_zero(available_quantity,
                                                                                     precision_rounding=rounding):
                break
        return reserved_quants

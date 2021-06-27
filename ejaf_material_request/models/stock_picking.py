from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_request_id = fields.Many2one('material.request', string='Material Request')

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
                            'location_dest_id': picking.picking_type_id.default_location_dest_id.id
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

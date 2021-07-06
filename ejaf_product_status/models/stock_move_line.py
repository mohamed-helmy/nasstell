# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status')

    @api.onchange('lot_id')
    def _set_product_status(self):
        if self.lot_id and self.lot_id.product_status:
            self.product_status = self.lot_id.product_status

    def _action_done(self):
        for move_line in self:
            if move_line.lot_id and move_line.product_status:
                move_line.lot_id.product_status = move_line.product_status
        res = super(StockMoveLine, self)._action_done()
        return res

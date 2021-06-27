# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status',related='lot_id.product_status')

    @api.onchange('lot_id')
    def _set_product_status(self):
        for line in self:
            if line.lot_id and line.lot_id.product_status:
                line.product_status = line.lot_id.product_status

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        if self.lot_id and self.product_status:
            self.lot_id.product_status = self.product_status
        return res

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status',related='lot_id.product_status')

    @api.onchange('lot_id')
    def _set_product_status(self):
        if self.lot_id and self.lot_id.product_status:
            self.product_status = self.lot_id.product_status


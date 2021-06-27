# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status')

    @api.onchange('prod_lot_id')
    def _set_product_status(self):
        for line in self:
            if line.prod_lot_id and line.prod_lot_id.product_status:
                line.product_status = line.prod_lot_id.product_status


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_validate(self):
        res = super(StockInventory, self).action_validate()
        for record in self:
            for line in record.line_ids:
                if line.prod_lot_id and line.product_status:
                    line.prod_lot_id.product_status = line.product_status
        return res

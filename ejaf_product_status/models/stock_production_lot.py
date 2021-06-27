# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_status = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('bad', 'Bad'), ('used', 'Used')],
                                      string='Product Status', default='normal')

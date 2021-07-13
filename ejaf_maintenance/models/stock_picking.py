# -*- coding: utf-8 -*-
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    job_order_id = fields.Many2one(comodel_name="maintenance.job.order")

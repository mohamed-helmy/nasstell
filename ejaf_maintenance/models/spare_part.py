# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class SparePart(models.Model):
    _name = 'spare.part'
    _rec_name = 'name'
    _description = 'Spare Part'

    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name="product.product", string="Item", required=True)
    product_qty = fields.Float(string="QTY")
    job_order_id = fields.Many2one(comodel_name="maintenance.job.order")

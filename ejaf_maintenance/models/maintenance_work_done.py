# -*- coding: utf-8 -*-
from odoo import models, fields


class WorkDone(models.Model):
    _name = 'maintenance.work.done'
    _rec_name = 'description'
    _description = 'Maintenance Work Done'

    description = fields.Char(string="Description", required=True)
    date = fields.Date()
    job_order_id = fields.Many2one(comodel_name="maintenance.job.order")

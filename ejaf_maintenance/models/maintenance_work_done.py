# -*- coding: utf-8 -*-
from odoo import models, fields


class MaintenanceWorkDone(models.Model):
    _name = 'maintenance.work.done'
    _rec_name = 'description'
    _description = 'Maintenance Work Done'

    description = fields.Char(string="Description", required=True)
    date = fields.Date(string='Date')
    job_order_id = fields.Many2one(comodel_name="maintenance.job.order")

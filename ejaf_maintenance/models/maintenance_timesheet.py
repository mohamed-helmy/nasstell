# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class MaintenanceTimesheet(models.Model):
    _name = 'maintenance.timesheet'
    _description = 'Maintenance Timesheet'

    name = fields.Char(string="Name", required=True)
    task_description = fields.Char(string="Task Description")
    duration = fields.Char(string="Duration(D:H)", compute='_compute_duration')
    cost = fields.Float(string="Cost")
    order_check_in = fields.Datetime(string="Check In")
    order_check_out = fields.Datetime(string="Check Out", )
    job_order_id = fields.Many2one(comodel_name="maintenance.job.order")

    @api.depends('order_check_in', 'order_check_out')
    def _compute_duration(self):
        for record in self:
            record.duration = False
            if record.order_check_in and record.order_check_out:
                date_difference = record.order_check_out - record.order_check_in
                record.duration = str(date_difference.days) + ":" + str(round(date_difference.seconds / 3600))

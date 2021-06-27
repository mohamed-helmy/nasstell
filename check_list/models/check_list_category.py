# -*- coding: utf-8 -*-
from odoo import models, fields


class CheckListCategory(models.Model):
    _name = 'check.list.category'
    _description = "Check List Category"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    is_generator = fields.Boolean(string='Generator?')

    def toggle_active(self):
        for record in self:
            record.active = not record.active
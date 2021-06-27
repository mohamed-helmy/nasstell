# -*- coding: utf-8 -*-
from odoo import models, fields


class CheckList(models.Model):
    _name = 'check.list'
    _description = "Check List"

    name = fields.Char(string="Name", required=True)
    check_list_question_ids = fields.One2many(comodel_name="check.list.question",
                                              inverse_name="check_list_id", string="Questions")

    type = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')], string='Type')
    is_default = fields.Boolean(string='Default?')
    is_mandatory = fields.Boolean(string='Mandatory?')

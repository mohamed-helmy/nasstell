# -*- coding: utf-8 -*-
from odoo import models, fields


class CheckList(models.Model):
    _inherit = 'check.list'

    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')

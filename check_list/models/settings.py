# -*- coding: utf-8 -*-
from odoo import api, models, fields


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    check_list_id = fields.Many2one(comodel_name="check.list", string="CheckList")

    @api.model
    def get_values(self):
        res = super(ResConfig, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            check_list_id=int(params.get_param('check_list.check_list_id'))
        )
        return res

    def set_values(self):
        super(ResConfig, self).set_values()
        ir_parameter = self.env['ir.config_parameter'].sudo()
        ir_parameter.set_param('check_list.check_list_id', self.check_list_id.id)

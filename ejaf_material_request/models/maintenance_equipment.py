# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import http, modules, SUPERUSER_ID, tools, _


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    material_request_count = fields.Integer(compute='calc_material_requests')
    returned_material_request_count = fields.Integer(compute='calc_returned_material_requests')

    def calc_material_requests(self):
        for rec in self:
            rec.material_request_count = self.env['material.request'].search_count(
                [('site_id', '=', rec.id), ('returned', '=', False)])

    def action_view_material_requests(self):
        return {
            'name': _('Material Requests'),
            'res_model': 'material.request',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_material_request.material_request_tree_view').id, 'tree'),
                (self.env.ref('ejaf_material_request.material_request_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('site_id', '=', self.id), ('returned', '=', False)],
            'context': {'default_returned': False,
                        'default_site_id': self.id}
        }

    def calc_returned_material_requests(self):
        for rec in self:
            rec.returned_material_request_count = self.env['material.request'].search_count(
                [('site_id', '=', rec.id), ('returned', '=', True)])

    def action_view_returned_material_requests(self):
        return {
            'name': _('Returned Material Requests'),
            'res_model': 'material.request',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_material_request.material_request_tree_view').id, 'tree'),
                (self.env.ref('ejaf_material_request.material_request_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('site_id', '=', self.id), ('returned', '=', True)],
            'context': {'default_returned': True,'default_site_id': self.id}
        }

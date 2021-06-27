# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    equipment_map_address = fields.Char('Map Address', tracking=True)
    equipment_latitude = fields.Float(string='Geo Latitude', digits=(16, 5), tracking=True)
    equipment_longitude = fields.Float(string='Geo Longitude', digits=(16, 5), tracking=True)
    color = fields.Selection(related='category_id.color', readonly=True, store=True, tracking=True)

    def update_location(self, latitude=0.0, longitude=0.0, record=None):
        for rec in self:
            rec.write({
                'equipment_latitude': latitude,
                'equipment_longitude': longitude
            })

    def init_map_location(self):
        for rec in self:
            return {
                'lat': rec.equipment_latitude,
                'lng': rec.equipment_longitude,

            }

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    request_map_address = fields.Char('Map Address', tracking=True)
    request_latitude = fields.Float(string='Geo Latitude', digits=(16, 5), tracking=True)
    request_longitude = fields.Float(string='Geo Longitude', digits=(16, 5), tracking=True)

    def update_location(self, latitude=0.0, longitude=0.0, record=None):
        for rec in self:
            rec.write({
                'request_latitude': latitude,
                'request_longitude': longitude
            })
            rec.action_timer_start()

    def init_map_location(self):
        return {
            'lat': self.request_latitude,
            'lng': self.request_longitude,

        }

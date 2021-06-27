from odoo import api, fields, models


class FiberConnection(models.Model):
    _name = 'fiber.connection'
    _rec_name = 'name'

    name = fields.Char()

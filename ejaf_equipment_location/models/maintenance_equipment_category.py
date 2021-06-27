# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class Equipment(models.Model):
    _inherit = 'maintenance.equipment.category'

    color = fields.Selection(
        string='Color',
        selection=[
            ('black', 'black'),
            ('blue', 'blue'),
            ('brown', 'brown'),
            ('cyan', 'cyan'),
            ('fuchsia', 'fuchsia'),
            ('green', 'green'),
            ('lime', 'lime'),
            ('maroon', 'maroon'),
            ('navy', 'navy'),
            ('olive', 'olive'),
            ('orange', 'orange'),
            ('pink', 'pink'),
            ('purple', 'purple'),
            ('red', 'red'),
            ('teal', 'teal'),
            ('white', 'white'),
            ('yellow', 'yellow'),
        ],
        default='red'
    )
    
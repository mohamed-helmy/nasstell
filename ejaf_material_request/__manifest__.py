# -*- coding: utf-8 -*-
{
    'name': "Ejaf Material Request",
    'summary': "Ejaf Material Request",
    'description': """add  material request in maintenance.
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",
    'depends': ['ejaf_product_status', 'ejaf_maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/material_request.xml',
        'views/res_config_settings.xml',
        'views/maintenance_request.xml',
        'views/stock_picking.xml',
        'views/maintenance_equipment.xml',

    ],
    'demo': [
    ],

}

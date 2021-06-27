# -*- coding: utf-8 -*-
{
    'name': "Ejaf Product Status",
    'summary': "Ejaf Product Status",
    'description': """add  product status to lot and serial.
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",
    'depends': ['stock'],
    'data': [
        'views/stock_production_lot.xml',
        'views/stock_quant.xml',
        'views/stock_inventory_line.xml',
        'views/stock_move.xml'
    ],
    'demo': [
    ],

}

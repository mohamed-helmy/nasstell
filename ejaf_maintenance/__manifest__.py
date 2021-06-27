# -*- coding: utf-8 -*-
{
    'name': "Ejaf Maintenance",
    'summary': """ """,
    'description': """
    ADD maintenance Job order
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",
    'version': '13.1',
    'depends': ['stock', 'check_list', 'ejaf_maintenance_equipment'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/maintenance_views.xml',
        'views/check_list_views.xml',
        'views/maintenance_job_order_view.xml',
        'views/technical_inspection_view.xml',
    ],
    'demo': [
    ],

}

# -*- coding: utf-8 -*-
{
    'name': "Ejaf SLA Maintenance",
    'summary': "Ejaf SLA Maintenance",
    'description': """add  sla policy in maintenance.
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",

    'depends': ['base', 'ejaf_maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/sla_policy.xml',
        'views/maintenance_request.xml',
        'views/menuitems.xml',
    ]

}

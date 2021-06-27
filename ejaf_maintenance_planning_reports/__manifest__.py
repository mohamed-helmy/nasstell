# -*- coding: utf-8 -*-
{
    'name': "Ejaf Maintenance Planning Reports",
    'summary': "Ejaf Maintenance Planning Reports",
    'description': """add  maintenance planning reports to equipment module
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",

    'depends': ['ejaf_maintenance', 'ejaf_maintenance_menus', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/activity.xml',
        'views/maintenance_planning_reports.xml',
        'views/menuitems.xml',
    ],
    

}

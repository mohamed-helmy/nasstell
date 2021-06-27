
# -*- coding: utf-8 -*-
{
    'name': 'Ejaf Equipment Location',
    'depends': [
        'ejaf_maintenance_equipment',
        'web_google_maps'

    ],
    "description": """
    Add Geo location to Equipment and Maintenance Request
   """,
    'author': "Ejaftech",
    'qweb': ['static/src/xml/*.xml'],

    'data': [
        'views/equipment_views.xml',
    ],
    'installable': True,
    'application': False,
}

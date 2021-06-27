# -*- coding: utf-8 -*-
{
    'name': "Check List",
    'description': """ add checklist in maintenance.
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",
    'depends': ['maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/check_list_view.xml',
        'views/check_list_category_view.xml',
        'views/check_list_question_view.xml',
        'views/res_settings_view.xml',
    ],
    'demo': [
    ],

}

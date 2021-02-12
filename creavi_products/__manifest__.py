# -*- coding: utf-8 -*-
{
    'name': "creavi_products",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','contacts','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sell_order_views.xml',
        'views/views_machine.xml',
        'views/views_accessoire.xml',
        'views/views_support.xml',
        'views/views_encre.xml',
        'views/views_settings.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

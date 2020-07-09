# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Pipedrive',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'mail', 'mail_activity_done'],
    'external_dependencies': {
        'python3' : ['pipedrive-python-lib', 'boto3'],
    },
    'data': [
        'data/ir_configparameter_data.xml',
        'data/ir_cron.xml',
        'views/pipedrive_menu.xml',
        'views/pipedrive_activity.xml',
        'views/pipedrive_activity_type.xml',
        'views/pipedrive_currency.xml',
        'views/pipedrive_deal.xml',
        'views/pipedrive_organization.xml',
        'views/pipedrive_person.xml',
        'views/pipedrive_pipeline.xml',
        'views/pipedrive_product.xml',
        'views/pipedrive_stage.xml',
        'views/pipedrive_user.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
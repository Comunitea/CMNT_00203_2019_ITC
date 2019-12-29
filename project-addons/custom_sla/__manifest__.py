# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom Sla',
    'summary': "Custom developemnts for Conecta",
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'base', 
        'contract', 
        'project',
        'sale',
        'custom_timecontrol_dates',
        'sale_contract_project_link'],
    'data': [
        'security/ir.model.access.csv',
        'data/project_sla_control_data.xml',
        'views/contract.xml',
        'views/project_sla_view.xml',
        'views/project_task_view.xml',
        'views/project_view.xml',
        'views/project_sla_control_view.xml',
        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}

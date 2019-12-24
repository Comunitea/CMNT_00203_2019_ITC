# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom timecontrol dates',
    'summary': "Custom developemnts for Conecta",
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'analytic', 
        'account', 
        'hr_timesheet',
        'contract',
    ],
    'data': [
        'data/mail_data.xml',
        'views/account_analytic_line_view.xml',
        'views/contract_view.xml',
        'views/project_task_view.xml',
        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}

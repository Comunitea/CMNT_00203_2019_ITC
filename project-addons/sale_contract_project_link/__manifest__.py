# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Contract Project Link',
    'summary': "Link Sales Contract & Projects",
    'version': '12.0.0.0.0',
    'category': 'Project',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': ['sale_timesheet', 'product_contract', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
        'views/project_view.xml',
        'views/contract.xml',
        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}

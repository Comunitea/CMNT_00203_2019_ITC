# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    @api.depends('project_id', 'project_id.analytic_account_id')
    def _get_contract_id(self):
        for task in self:
            if task.project_id and task.project_id.analytic_account_id:
                ac_id = task.project_id.analytic_account_id.id
                domain = [('group_id', '=', ac_id)]
                contract = self.env['contract.contract'].search(domain, limit=1)
                if contract:
                    task.contract_id = contract.id

    contract_id = fields.Many2one(
        'contract.contract', compute='_get_contract_id', store=True)
    is_issue = fields.Boolean('Is issue', default=True)
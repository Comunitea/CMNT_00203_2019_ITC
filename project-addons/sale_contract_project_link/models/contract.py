# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _compute_task_issue_count(self):
        for contract in self:
            domain = [('contract_id', '=', contract.id), ('is_issue', '=', True)]
            task_count = self.env['project.task'].search_count(domain)
            contract.task_issue_count = task_count

    project_id = fields.Many2one('project.project', string='Project')
    task_issue_count = fields.Integer(
        compute='_compute_task_issue_count', string="Task Count")

    _sql_constraints = [
        ('unique_group_id', 'unique(group_id)', 
          _('Analytic account already assigned')),
        ('unique_project_id', 'unique(project_id)', 
         _('Projectt already assigned')),
    ]

    @api.multi
    def _get_project_vals(self):
        self.ensure_one()
        res = {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'allow_timesheets': True,  # To create analytic account id
            'company_id': self.company_id.id,
        }

        return res

    @api.multi
    def link_project(self, recalc_closed=False):
        Project = self.env['project.project']
        for contract in self:
            if contract.project_id:
                continue
            vals = contract._get_project_vals()
            project = Project.create(vals)
            contract.write({
                'project_id': project.id,
                'group_id': project.analytic_account_id.id
            })
            project.get_contract_id()

        return True


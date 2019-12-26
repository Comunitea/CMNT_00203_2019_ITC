# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def get_contract_id(self):
        for project in self:
            if project.analytic_account_id:
                ac_id = project.analytic_account_id.id
                domain = [('group_id', '=', ac_id)]
                contract = self.env['contract.contract'].search(domain, 
                                                                limit=1)
                if contract:
                    project.contract_id = contract.id
    
    def _compute_task_issue_count(self):
        for project in self:
            domain = [('project_id', '=', project.id), ('is_issue', '=', True)]
            task_count = self.env['project.task'].search_count(domain)
            project.task_issue_count = task_count

    task_issue_count = fields.Integer(
        compute='_compute_task_issue_count', string="Task Count")

    contract_id = fields.Many2one(
        'contract.contract', compute='get_contract_id', store=True)

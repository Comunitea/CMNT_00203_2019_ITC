# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = ['project.project']

    @api.multi
    def _hours_quantity(self):
        for project in self:
            hours_quantity = 0.0
            remaing_hours = 0.0
            discounted_hours = 0.0
            # hours_quantity = \
            #     round(sum(project.task_ids.mapped('effective_hours')), 2)

            domain = [('project_id', '=', project.id)]
            # if project.analytic_account_id:
            #     domain = [
            #         '|',
            #         ('account_id', '=', project.analytic_account_id.id),
            #         ('project_id', '=', project.id),
            #     ]
            a_lines = self.env['account.analytic.line'].search(domain)
            hours_quantity = \
                round(sum(a_lines.mapped('unit_amount')), 2)
            hours_discount = \
                round(sum(a_lines.mapped('discount')), 2)
            project.hours_quantity = hours_quantity
            project.remaining_hours = \
                project.quantity_max - hours_quantity
            project.total_discount = hours_discount
    
    @api.multi
    def _get_discounted(self):
        for project in self:
            domain = [
                ('task_id', 'in', project.task_ids.ids)]
            lines = self.env['account.analytic.line'].search(domain)
            tot_disc = round(sum(lines.mapped('discount')), 2)
            project.total_discount = tot_disc
    
    quantity_max = fields.Float('Scheduled Time')
    hours_quantity = fields.Float(
        'Total Worked Time', compute='_hours_quantity')
    remaining_hours = fields.Float(
        'Remaining Time', compute='_hours_quantity')
    total_discount = fields.Float(
        'Total Discounted Time', compute='_get_discounted')
    
    def write(self, vals):
        res = super().write(vals)
        if vals.get('quantity_max'):
            qm = vals['quantity_max']
            if self.contract_id and self.contract_id.quantity_max != qm:
                self.contract_id.write({
                    'quantity_max': qm})
        return res

    

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
            hours_quantity = \
                round(sum(project.task_ids.mapped('effective_hours')), 2)
            project.hours_quantity = hours_quantity
            project.remaining_hours = \
                project.quantity_max - hours_quantity
    
    @api.multi
    def _get_discounted(self):
        for project in self:
            domain = [
                ('task_id', 'in', project.task_ids.ids)]
            lines = self.env['account.analytic.line'].search(domain)
            tot_disc = round(sum(lines.mapped('discount')), 2)
            project.total_discount = tot_disc
    
    quantity_max = fields.Float('Scheduled Time')
    hours_quantity = fields.Float('Total Worked Time', compute='_hours_quantity')
    remaining_hours = fields.Float('Remaining Time', compute='_hours_quantity')
    total_discount = fields.Float('Total Discounted Time', compute='_get_discounted')
    

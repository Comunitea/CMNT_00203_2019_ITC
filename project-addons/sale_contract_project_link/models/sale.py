# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    def action_confirm(self):
        """ If we have a contract in the order, set it up """
        res = super().action_confirm()
        for order in self:
            contracts = (
                self.env['contract.line']
                .search([('sale_order_line_id', 'in', order.order_line.ids)])
                .mapped('contract_id')
            )
            projects = self.project_ids
            if projects and projects[0].analytic_account_id and contracts:
                project = projects[0]
                contracts.write(
                    {'group_id': projects[0].analytic_account_id.id,
                     'project_id':project.id
                    })
        return res

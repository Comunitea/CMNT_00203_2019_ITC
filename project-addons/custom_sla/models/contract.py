# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ContractContract(models.Model):
    _inherit = "contract.contract"

    sla_ids = fields.Many2many('project.sla', string='Service Level Agreement')

    @api.multi
    def _reapply_sla(self, recalc_closed=False):
        ctrl_obj = self.env['project.sla.control']
        for contract in self:
            # for each contract, and for each model under SLA control ...

            ctrl_models = set([sla.control_model for sla in contract.sla_ids])
            for model_name in ctrl_models:
                model = self.env[model_name]
                base = []
                # base = [] if recalc_closed else [('stage_id.fold', '=', 0)]
                doc_ids = []
                # if 'analytic_account_id' in model._columns:
                #     domain = base + [
                #         ('analytic_account_id', '=', contract.id)]
                #     doc_ids += model.search(cr, uid, domain, context=context)

                docs = self.env[model_name]
                if 'project_id' in model._fields:
                    domain = base + [
                        ('project_id.analytic_account_id', '=', contract.group_id.id)]
                    docs += model.search(domain)
                if docs:
                    ctrl_obj.store_sla_control(docs)
        return True
    
    def reapply_sla(self):
        return self._reapply_sla()

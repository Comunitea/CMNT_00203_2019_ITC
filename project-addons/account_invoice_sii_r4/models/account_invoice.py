# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoce(models.Model):

    _inherit = "account.invoice"


    @api.multi
    def get_taxes_values(self):
        tax_grouped = super().get_taxes_values()
        if self.sii_refund_specific_invoice_type == 'R4':
            for tax in tax_grouped.values():
                tax['base'] = 0
        return tax_grouped
    
    
class AccountInvoceTax(models.Model):

    _inherit = "account.invoice.tax"

    @api.depends('invoice_id.invoice_line_ids', 'invoice_id.sii_refund_specific_invoice_type')
    def _compute_base_amount(self):
        return super()._compute_base_amount()
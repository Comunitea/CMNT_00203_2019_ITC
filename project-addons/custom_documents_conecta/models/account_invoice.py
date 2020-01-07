from odoo import models, api, fields
from odoo.tools import formatLang, format_date


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    def _get_invoice_line_name_from_product(self):
        """ Returns the automatic name to give to the invoice line depending on
        the product it is linked to.
        """        
        res = super()._get_invoice_line_name_from_product()
        if not self.product_id:
            return ""
        
        res = self.product_id.name
        return res
    
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # Sobrescribo para sacar la fecha con - y el separador un - tambien
    def get_expiration_dates_list(self, padding, signed):
        sign = 1
        if signed and 'refund' in self.type:
            sign = -1
        self.ensure_one()
        expiration_dates = []
        if self.move_id:
            move_lines = self.env["account.move.line"].\
                search([('move_id', '=', self.move_id.id),
                        ('account_id.internal_type', 'in',
                            ['payable', 'receivable']),
                        ('date_maturity', "!=", False)],
                       order="date_maturity asc")
            for line in move_lines:
                currency = self.currency_id
                if self.type in ('out_invoice', 'in_refund'):
                    quantity = formatLang(
                        self.env, sign * line.debit, currency_obj=currency)
                else:
                    quantity = formatLang(self.env, sign * line.credit)
                expiration_dates.append('{} {} {}'.format(
                    line.date_maturity.strftime('%d-%m-%Y'), ' - ' * padding,
                    quantity))
        return expiration_dates
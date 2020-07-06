# -*- coding: utf-8 -*-

from odoo import models,api


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'
    
    @api.multi
    def send_and_print_action(self):
        if not(self.composition_mode == 'mass_mail' and self.template_id):
            self.onchange_template_id()
        return super().send_and_print_action()
    
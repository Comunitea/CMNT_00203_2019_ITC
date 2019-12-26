# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    did_customer = fields.Boolean(string='D&D customer')
    legal_representative = fields.Char(string='Legal representant')
    nif_representative = fields.Char (string='Representant nif')
    date = fields.Date(string='Date')

    timetable = fields.Char('Customer timesheet')
    # notify_email =  fields.Selection([
    #     ('none', 'Never'),
    #     ('always', 'All Messages'),
    #     ], 'Receive Inbox Notifications by Email', required=True,
    #     oldname='notification_email_send',
    #     default='none')
    gestor_id = fields.Many2one('res.partner', string='Gestor', 
        domain="[('es_gestor','=', True)]")
    invoice_picking = fields.Boolean(
        'Send invoice to customer when we do a picking for him')
    
    #en pantalla general
    is_gestor = fields.Boolean(string='Is gestor')
    nima_code = fields.Char(string = 'NIMA code')
    rp = fields.Char(string = 'RP code')
    rnp = fields.Char(string = 'RNP code')
    
    #a poner en pestaa nueva
    translate_partner = fields.Char(string='Translate Partner')
    translate_address = fields.Char(string='Translate Address')
    translate_cif = fields.Char(string='Cif')
    nima_translate = fields.Char(string='Cod nima')
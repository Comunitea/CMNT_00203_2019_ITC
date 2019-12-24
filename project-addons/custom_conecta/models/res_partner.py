# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    did_customer = fields.Boolean(string='Cliente D&D')
    legal_representative = fields.Char(string='Representante Legal')
    nif_representative = fields.Char (string='Nif del representante')
    date = fields.Date(string='Fecha')

    timetable = fields.Char('Horario del cliente')
    # notify_email =  fields.Selection([
    #     ('none', 'Never'),
    #     ('always', 'All Messages'),
    #     ], 'Receive Inbox Notifications by Email', required=True,
    #     oldname='notification_email_send',
    #     default='none')
    gestor_id = fields.Many2one('res.partner', string='Gestor', 
        domain="[('es_gestor','=', True)]")
    invoice_picking = fields.Boolean(
        'Enviar factura a este cliente cuando se realiza un \
        albaran en su nombre')
    
    #en pantalla general
    is_gestor = fields.Boolean(string='Es gestor')
    nima_code = fields.Char(string = 'Codigo NIMA')
    rp = fields.Char(string = 'Codigo RP')
    rnp = fields.Char(string = 'Codigo RNP')
    
    #a poner en pestaa nueva
    translate_partner = fields.Char(string = 'Empresa')
    translate_address = fields.Char(string = 'Dirección')
    translate_cif = fields.Char(string = 'Cif')
    nima_translate = fields.Char(string = 'Cod nima')
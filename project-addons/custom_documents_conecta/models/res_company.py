from odoo import models, api, fields

class Company(models.Model):
    _inherit = "res.company"
    
    logo_footer_left = fields.Binary('Footer Logo Left')
    logo_footer_rigth = fields.Binary('Footer Logo Right')
    logo_lopd = fields.Binary('Lpd Logo')
    sale_note = fields.Text('Sales Notes')
    invoice_text = fields.Text('Invoice Text')
    lopd_text = fields.Text('Lopd Text')
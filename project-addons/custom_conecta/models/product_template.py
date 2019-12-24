# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    gestor_product = fields.Float('Gestor product')

    ler_code = fields.Char(string="Codigo LER")
    waste_type = fields.Selection(
        [('papel', 'Papel'),
         ('toner', 'Toner'), ('raees', 'Raees')], 
        string='Tipo residuo')
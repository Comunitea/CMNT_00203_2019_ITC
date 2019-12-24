# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    did_weight = fields.Float('Peso Contenedor')
    part_state = fields.Selection(
        [('a', 'Aceptado'), ('r', 'Rechazado')],
        string='Estado del parte')
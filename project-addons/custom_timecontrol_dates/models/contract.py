# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api



class Contract(models.Model):
    _inherit = "contract.contract"

    signature = fields.Binary("Firma del cliente")
    warn_percent = fields.Float(
        "Porcentaje límite para avisos", default=0.7)

    @api.multi
    def check_limit(self):
        # TODO
        flag = False
        # for contract in self:
        #     if contract.quantity_max:
        #         if contract.remaining_hours <= \
        #                 contract.quantity_max * (1 - contract.warn_percent) and \
        #                 contract.warn_percent > 0:
        #             flag = True
        return flag


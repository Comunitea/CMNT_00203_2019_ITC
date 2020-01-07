from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    

    # Sobrescribo para que no se pase el nombre a la venta con corchetes
    def get_sale_order_line_multiline_description_sale(self, product):
        name = ""
        if self.product_id:
            name += self.product_id.name
            if self.product_id.description_sale:
                    name += '\n' + self.description_sale
        return name    
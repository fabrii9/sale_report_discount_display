# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # -------------------------------------------------------------------------
    # Monto total de descuento aplicado (en base imponible, sin impuestos)
    #
    # Lógica:
    #   amount_undiscounted = suma de (price_subtotal sin descuento) por línea
    #     → ya existe en sale.order core: suma de price_unit*qty sin aplicar discount
    #   amount_untaxed       = suma de price_subtotal (con descuento, sin impuestos)
    #   → diferencia = monto descontado en base imponible
    #
    # Consistencia del display en el PDF:
    #   Total sin descuento (tachado) = amount_undiscounted + amount_tax
    #   Total a pagar                 = amount_total  (= amount_untaxed + amount_tax)
    #   Descuento aplicado            = amount_discount_total
    #
    #   Verificación aritmética:
    #   (amount_undiscounted + amount_tax) - (amount_undiscounted - amount_untaxed)
    #   = amount_tax + amount_untaxed = amount_total ✓
    # -------------------------------------------------------------------------
    amount_discount_total = fields.Monetary(
        string='Descuento aplicado',
        compute='_compute_amount_discount_total',
        store=False,  # Siempre recalcular para evitar problemas con pedidos existentes
        currency_field='currency_id',
    )

    @api.depends(
        'order_line.discount',
        'order_line.price_subtotal',
        'order_line.price_unit',
        'order_line.product_uom_qty',
        'amount_untaxed',
    )
    def _compute_amount_discount_total(self):
        for order in self:
            amount_undiscounted = 0.0
            for line in order.order_line.filtered(lambda l: not l.display_type):
                if line.discount == 100.0:
                    amount_undiscounted += line.price_unit * line.product_uom_qty
                elif line.discount:
                    amount_undiscounted += (
                        line.price_subtotal * 100.0 / (100.0 - line.discount)
                    )
                else:
                    amount_undiscounted += line.price_subtotal
            order.amount_discount_total = amount_undiscounted - order.amount_untaxed

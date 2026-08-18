# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # -------------------------------------------------------------------------
    # Montos del bloque de descuento en el PDF (todos CON impuestos incluidos,
    # para que Total sin descuento - Descuento = Total a pagar).
    #
    # Lógica:
    #   amount_total_undiscounted = suma por línea del total CON impuestos
    #     calculado sobre price_unit * qty SIN aplicar el descuento, usando
    #     tax_id.compute_all() para respetar impuestos incluidos en precio,
    #     múltiples alícuotas, exenciones, etc.
    #   amount_discount_total     = amount_total_undiscounted - amount_total
    #
    # Consistencia del display en el PDF:
    #   Total sin descuento (tachado) = amount_total_undiscounted
    #   Total a pagar                 = amount_total
    #   Descuento aplicado            = amount_discount_total
    #   → tachado - descuento = total a pagar ✓ (todos en la misma base)
    #
    # NOTA: no usar doc.amount_undiscounted + doc.amount_tax como total
    # tachado: mezcla la base sin descuento con el IVA calculado sobre la
    # base CON descuento, y da un número que no existe.
    # -------------------------------------------------------------------------
    amount_total_undiscounted = fields.Monetary(
        string='Total sin descuento',
        compute='_compute_amount_discount_total',
        store=False,  # Siempre recalcular para evitar problemas con pedidos existentes
        currency_field='currency_id',
    )
    amount_discount_total = fields.Monetary(
        string='Descuento aplicado',
        compute='_compute_amount_discount_total',
        store=False,
        currency_field='currency_id',
    )
    # Porcentaje ya formateado para el PDF ("25", "12,5"), sin ceros de más
    discount_percent_label = fields.Char(
        string='% de descuento',
        compute='_compute_amount_discount_total',
        store=False,
    )

    @api.depends(
        'order_line.discount',
        'order_line.price_unit',
        'order_line.product_uom_qty',
        'order_line.tax_id',
        'amount_total',
    )
    def _compute_amount_discount_total(self):
        for order in self:
            total_undiscounted = 0.0
            for line in order.order_line.filtered(lambda l: not l.display_type):
                taxes = line.tax_id.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.product_uom_qty,
                    product=line.product_id,
                    partner=order.partner_shipping_id,
                )
                total_undiscounted += taxes['total_included']
            discount_total = total_undiscounted - order.amount_total
            order.amount_total_undiscounted = total_undiscounted
            order.amount_discount_total = discount_total
            if total_undiscounted > 0 and discount_total > 0:
                pct = round(discount_total / total_undiscounted * 100.0, 2)
                order.discount_percent_label = (
                    ('%f' % pct).rstrip('0').rstrip('.').replace('.', ',')
                )
            else:
                order.discount_percent_label = False

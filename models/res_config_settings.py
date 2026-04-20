# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_report_show_discount = fields.Boolean(
        string='Mostrar descuento aplicado en el PDF del presupuesto',
        config_parameter=False,
        related='company_id.sale_report_show_discount',
        readonly=False,
    )

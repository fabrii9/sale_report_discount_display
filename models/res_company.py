# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_report_show_discount = fields.Boolean(
        string='Mostrar descuento en presupuesto PDF',
        default=True,
    )

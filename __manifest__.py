# -*- coding: utf-8 -*-
{
    'name': 'Presupuesto PDF - Mostrar Descuento Aplicado',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Muestra de forma comercial el descuento total en el PDF del presupuesto.',
    'description': """
        Modifica la visualización del bloque de totales en el reporte PDF del presupuesto (sale.order),
        mostrando el descuento de forma clara y atractiva para el cliente:

        - Total sin descuento (tachado)
        - Total a pagar (destacado en negrita)
        - Descuento aplicado (en verde)

        Si el pedido no tiene ningún descuento, se mantiene el diseño estándar de Odoo.
    """,
    'author': 'Custom - Cortinas Argentinas',
    'depends': ['sale', 'l10n_ar_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'report/report_saleorder_discount.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def action_purchase_order_confirm_and_delivery(self):
        self.button_confirm()

        for picking in self.picking_ids:

            for line in picking.move_lines:
                line.quantity_done = line.product_uom_qty

            picking.button_validate()

    @api.multi
    def action_purchase_order_confirm_and_invoiced(self):
        self.action_purchase_order_confirm_and_delivery()

        self.with_context(create_bill=True).action_view_invoice()

        for invoice in self.invoice_ids:
            invoice.action_invoice_open()

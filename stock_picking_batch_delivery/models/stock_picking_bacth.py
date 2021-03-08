# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging


class StockPickingBatch(models.Model):
    _inherit = ['stock.picking.batch']

    delivery_id = fields.Many2one('delivery.carrier', string='Método de entrega')

    date_planned = fields.Datetime(
        'Fecha', default=fields.Datetime.now, index=True, required=True,
        states={'done': [('readonly', True)]})

    total_weight = fields.Float(compute='compute_total_weight', string='Peso Total')

    @api.depends('picking_ids')
    def compute_total_weight(self):
        for picking_id in self.picking_ids:
            if picking_id.weight != 0.00:
                self.total_weight+=picking_id.weight
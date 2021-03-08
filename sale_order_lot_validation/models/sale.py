from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super().action_confirm()
        for so in self:
            for line in so.order_line.filtered(lambda l: l.product_id.tracking == 'lot'):
                if not line.lot_id:
                    raise UserError(
                        _('You can\'t store this line %s with empty lot') %
                        line.product_id.name
                        )
                product_lot_qty = 0
                if so.warehouse_id and line.product_id:
                    quants = self.env['stock.quant'].search([
                        ('location_id', 'child_of', so.warehouse_id.lot_stock_id.id),
                        ('product_id', '=', line.product_id.id),
                        ('lot_id', '=', line.lot_id.id),
                    ])
                    if quants:
                        product_lot_qty = sum(quants.mapped('quantity'))
                if product_lot_qty < line.product_uom_qty:
                    raise UserError(
                        _('Not enough stock in lot %s, only %.2f for product : %s') %
                        (line.lot_id.name, product_lot_qty, line.product_id.name )
                )
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    lot_id = fields.Many2one(
        'stock.production.lot',
        'Lot',
        copy=False
    )

    @api.onchange('product_uom_qty', 'lot_id', 'product_uom')
    def _onchage_quantity_or_lot(self):
        if not self.product_id:
            return
        if self.product_id.tracking != 'lot':
            return
        if not self.lot_id:
            return
        # get lot quantity
        product_lot_qty = 0
        if self.order_id.warehouse_id:
            quants = self.env['stock.quant'].search([
                ('location_id', 'child_of', self.order_id.warehouse_id.lot_stock_id.id),
                ('product_id', '=', self.product_id.id),
                ('lot_id', '=', self.lot_id.id),
            ])
            if quants:
                product_lot_qty = sum(quants.mapped('quantity'))
        product_uom_qty = self.product_uom_qty * self.product_uom.factor_inv
        if product_lot_qty < product_uom_qty:
            raise UserError(
                _('Not enough stock in lot %s, only %.2f for product : %s') %
                (self.lot_id.name, product_lot_qty, self.product_id.name )
                )

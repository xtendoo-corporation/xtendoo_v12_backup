# -- coding: utf-8 --


from odoo import api, models, fields
from odoo.exceptions import ValidationError
import logging


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    _name = 'account.invoice.line'

    is_admin = fields.Boolean(
        comodel_name='account.invoice.line',
        compute='_is_admin',
        string="isAdmin",
        default=lambda self: self._get_default_admin()
    )
    @api.one
    def _is_admin(self):
        self.is_admin=self.env.user.administration
        return

    @api.model
    def _get_default_admin(self):
        return self.env.user.administration

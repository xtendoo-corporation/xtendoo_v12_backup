from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import logging


class Users(models.Model):
    _inherit = "res.users"

    partner_ids = fields.One2many('res.partner', 'user_id')

    @api.multi
    def action_open_visits_routes(self):
        self.ensure_one()
        view = self.env.ref('partner_routes.partner_visit_day')

        return {'name': _('Visit'),
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'partner.visit.day',
                'view_id': view.id,
                'views': [(view.id, 'form')],
                'type': 'ir.actions.act_window',
                'context': {'default_user_id': self.id}}


class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('partner.visit', 'partner_id')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_default_partner(self):
        logging.info("@"*80)
        logging.info(self.env["partner.visit"].get_partner_visit_today())
        return 1

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True,
                                 change_default=True, index=True, track_visibility='always', track_sequence=1,
                                 help="You can find a customer by its Name, TIN, Email or Internal Reference.",
                                 default=_get_default_partner)

    has_outstanding = fields.Boolean()

    @api.multi
    def button_next_costumer(self):
        if self.partner_id:
            self.env["partner.visit.line"].create_if_not_exist(self.partner_id.id)

        partner_visit = self.env["partner.visit"].get_partner_visit_today()
        if not partner_visit:
            self.has_outstanding = True
            return

        self.partner_id = partner_visit.partner_id
        self.onchange_partner_id()

    @api.model
    def create(self, values):
        logging.info("Create a new sale order **************************************")
        res = super(SaleOrder, self).create(values)
        res.env["partner.visit.line"].write_sale_id(res.id, res.partner_id.id)
        return res


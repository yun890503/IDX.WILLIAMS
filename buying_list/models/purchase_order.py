from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_centralized = fields.Boolean(
        string="團購",
        default=False,
    )

    @api.onchange('state')
    def _onchange_editable_field(self):
        """控制欄位是否可編輯"""
        if self.state not in ['draft', 'purchase']:
            self.is_centralized = False

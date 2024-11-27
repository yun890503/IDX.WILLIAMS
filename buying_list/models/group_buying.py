from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
class GroupBuying(models.Model):
    _name = 'group.buying'
    _description = '團購表單'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='開團單號', required=True, readonly=True, default='New')
    user_id = fields.Many2one(
        'res.users',
        string='開團人員',
        default=lambda self: self.env.user,  
        required=True
    )
    user_email = fields.Char(
        string='開團人員 Email',
        related='user_id.partner_id.email',  # 從 res.partner 表的 email 帶出
        readonly=True
    )
    open_date = fields.Date(string='開團日期', required=True ,tracking=True)
    close_date = fields.Date(string='結單日期', required=True)
    active = fields.Boolean(string='有效', default=True)
    group_buying_ids = fields.One2many('group.buying.line', 'group_buying_id', string='團購表單明細')
    total_amount = fields.Integer(string='總計', compute='_compute_total_amount', store=True)

    @api.onchange('open_date')
    def _onchange_open_date(self):
        print(self)
        if self.open_date:
            self.close_date = self.open_date + timedelta(days=10)

    @api.depends('group_buying_ids.amount')
    def _compute_total_amount(self):
        print(self)
        for record in self:
            record.total_amount = sum(line.amount for line in record.group_buying_ids)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':  
            current_year = datetime.now().strftime('%y')  
            current_month = datetime.now().strftime('%m')  
            sequence_code = f"GB{current_year}{current_month}"  
            last_sequence = self.search([('name', 'like', f"{sequence_code}%")], order='name desc', limit=1)
            
            if last_sequence:
                last_number = int(last_sequence.name[-3:])  
                new_number = last_number + 1
            else:
                new_number = 1
            vals['name'] = f"{sequence_code}{str(new_number).zfill(3)}"  
        return super(GroupBuying, self).create(vals)

    @api.constrains('open_date', 'close_date')
    def _check_dates(self):
        for record in self:
            if record.close_date < record.open_date:
                raise ValidationError("開團日期需早於結單日期!")


class GroupBuyingLine(models.Model):
    _name = 'group.buying.line'
    _description = '團購表單明細'

    phone = fields.Char('電話號碼', related='partner_id.phone', readonly=True)
    group_buying_id = fields.Many2one('group.buying', string='開團單號', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='跟團人員', required=True)
    product_id = fields.Many2one('product.product', string='商品', required=True)
    unit_price = fields.Integer(string='單價')
    qty = fields.Integer(string='數量', required=True, default=1)
    amount = fields.Integer(string='金額', compute='_compute_amount', store=True )

    @api.depends('unit_price', 'qty')
    def _compute_amount(self):
        for line in self:
            line.amount = line.unit_price * line.qty

    @api.onchange('unit_price', 'qty')
    def _onchange_amount(self):
        if self.unit_price and self.qty:
            self.amount = self.unit_price * self.qty

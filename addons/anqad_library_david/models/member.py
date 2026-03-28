from odoo import models, fields, api

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    member_id = fields.Char(string='Member ID', readonly=True, copy=False)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    join_date = fields.Date(string='Join Date', default=fields.Date.today)
    active = fields.Boolean(string='Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('member_id'):
                vals['member_id'] = self.env['ir.sequence'].next_by_code('library.member')
        return super().create(vals_list)
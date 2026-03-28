from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow Transaction'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    borrow_date = fields.Date(string='Borrow Date', required=True, default=fields.Date.today)
    due_date = fields.Date(string='Due Date', required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], string='State', default='active')

    is_overdue = fields.Boolean(string='Overdue?', compute='_compute_is_overdue', store=True)

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_overdue = rec.state == 'active' and bool(rec.due_date) and rec.due_date < today

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            book = self.env['library.book'].browse(vals['book_id'])
            if book.available_copies < 1:
                raise ValidationError('No copies available for: ' + book.title)
            book.write({
                'available_copies': book.available_copies - 1,
                'state': 'borrowed',
            })
        return super().create(vals_list)

    def action_return(self):
        for rec in self:
            rec.book_id.write({
                'available_copies': rec.book_id.available_copies + 1,
                'state': 'available',
            })
            rec.write({'state': 'returned', 'return_date': fields.Date.today()})

    def _cron_mark_overdue(self):
        overdue = self.search([
            ('state', '=', 'active'),
            ('due_date', '<', fields.Date.today()),
        ])
        overdue.write({'state': 'overdue'})
        for rec in overdue:
            rec.member_id.message_post(
                body=f'Book "{rec.book_id.title}" is overdue since {rec.due_date}.'
            )
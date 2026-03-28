from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    title = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN')
    author_id = fields.Many2one('library.author', string='Author', required=True, ondelete='restrict')
    genre = fields.Selection([
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('other', 'Other'),
    ], string='Genre')
    publish_date = fields.Date(string='Publish Date')
    available_copies = fields.Integer(string='Available Copies', default=1)
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ], string='State', default='available')

    borrow_ids = fields.One2many('library.borrow', 'book_id', string='Borrows')
    total_borrows = fields.Integer(string='Total Borrows', compute='_compute_total_borrows')

    @api.depends('borrow_ids')
    def _compute_total_borrows(self):
        for book in self:
            book.total_borrows = len(book.borrow_ids)

    _sql_constraints = [
        ('unique_isbn', 'UNIQUE(isbn)', 'ISBN must be unique.')
    ]
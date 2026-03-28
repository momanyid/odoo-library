from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    biography = fields.Text(string='Biography')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Author name must be unique.')
    ]
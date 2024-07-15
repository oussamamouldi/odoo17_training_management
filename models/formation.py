from odoo import models, fields, api
class Formation(models.Model):
    _name = 'formation.formation'
    _description = 'Formation description'

    name = fields.Char(required=True)
    price = fields.Float()
    category = fields.Char()

    session_ids = fields.One2many('session.session', 'id', string='Sessions')
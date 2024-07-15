from odoo import models, fields, api
class Salle(models.Model):
    _name = 'salle.salle'
    _description = 'salle description'

    name = fields.Char(required=True)
    nb_places = fields.Integer()
    Free = fields.Boolean( default=True)
    session = fields.Many2many('session.session')
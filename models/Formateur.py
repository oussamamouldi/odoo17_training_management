from odoo import models, fields, api
class Formateur(models.Model):
    _name = 'formateur.formateur'
    _description = 'Formateur description'
    _sql_constraints = [
        ('matricule_unique', 'unique(matricule)', 'Maricule already exists !')
    ]

    name = fields.Char(required=True)
    matricule = fields.Integer()
    diplome = fields.Char()
    session = fields.Many2many('session.session')
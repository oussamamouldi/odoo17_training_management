
from odoo import models, fields, api


class Candidat(models.Model):
    _name = 'candidat.candidat'
    _description = 'Candidat description'
    _sql_constraints = [
        ('Num_ins_unique', 'Unique(num_ins)', 'Inscrription number already exists !')
    ]

    name = fields.Char( required=True)
    num_ins = fields.Integer("Inscription number")
    session = fields.Many2many('session.session')





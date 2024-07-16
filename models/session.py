from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Session(models.Model):
    _name = 'session.session'
    _description = 'Session Description'

    name = fields.Char(string='Session Name', required=True)
    nb_participants = fields.Integer(string='Number of Participants')
    nb_participants_max = fields.Integer(string='Number of Participants max', required=True)
    date_debut = fields.Datetime(string='Start Date')
    date_fin = fields.Datetime(string='End Date')
    duree = fields.Char(string='Duration', compute='compute_duree')
    # state = fields.Selection([], string='State')
    state = fields.Char(string='Duration', compute='compute_state')
    categorie = fields.Char(string='Category', compute='compute_category')

    formation_id = fields.Many2one('formation.formation', string='Formation', ondelete="cascade")
    salle_ids = fields.Many2many('salle.salle', 'session_salle', column1='session_id', column2='salle_id', string='Rooms')
    candidat_ids = fields.Many2many('candidat.candidat', 'session_candidat', column1='session_id', column2='candidat_id', string='Candidates')
    formateur_ids = fields.Many2many('formateur.formateur', 'session_formateur', column1='session_id', column2='formateur_id', string='Trainee')

    # def compute_nb_max(self):
    #     for session in self:
    #         if session.nb_participants_max>0 :
    #             return session.nb_participants_max
    #         else :
    #             session.nb_participants_max = False



    @api.depends('date_debut', 'date_fin')
    def compute_duree(self):
        for session in self:
            if session.date_debut and session.date_fin and session.date_validation:
                date_debut = fields.Datetime.from_string(session.date_debut)
                date_fin = fields.Datetime.from_string(session.date_fin)
                delta = date_fin - date_debut
                session.duree = str(delta.days) + ' days'
            else:
                session.duree = False

    @api.depends('formation_id')
    def compute_category(self):
        for session in self:
            if session.formation_id:
                session.categorie = session.formation_id.category
            else:
                session.categorie = False

    @api.constrains('date_debut', 'date_fin')
    def date_validation(self):
        for session in self:
            if session.date_debut and session.date_fin:
                date_debut = fields.Datetime.from_string(session.date_debut)
                date_fin = fields.Datetime.from_string(session.date_fin)
                if date_fin < date_debut:
                    raise ValidationError('End date cannot be earlier than start date!')



    @api.constrains('salle_ids')
    def nb_trainee_room_cap(self):
        for session in self:
            for salle in session.salle_ids:
                if session.nb_participants > salle.nb_places:
                    raise ValidationError('Room cannot handle the number of participants!')

    @api.depends('date_debut', 'date_fin')
    def compute_state(self):
        current_date = fields.Datetime.now()
        for session in self:
            if session.date_debut and session.date_fin:
                date_debut = fields.Datetime.from_string(session.date_debut)
                date_fin = fields.Datetime.from_string(session.date_fin)
                if current_date < date_debut:
                    session.state = 'Not started'
                elif current_date >= date_debut and current_date <= date_fin:
                    session.state = 'In action'
                elif current_date > date_fin:
                    session.state = 'Finished'
            else:
                session.state = 'Not started'

    @api.constrains('formateur_ids', 'date_debut', 'date_fin')
    def trainee_available(self):
        for session in self:
            if session.formateur_ids and session.date_debut and session.date_fin :
                lookfor =self.env['session.session'].search([
                ('id', '!=', session.id),
                ('formateur_ids' ,'in',session.formateur_ids.ids),
                ('date_debut','<=', session.date_fin),
                ('date_fin','>=', session.date_debut)
                ])
                if lookfor :
                    raise ValidationError('Trainer not available before session start!')

    @api.constrains('candidat_ids', 'date_debut', 'date_fin')
    def candidate_assigned(self):
         for session in self:
                if session.candidat_ids and session.date_debut and session.date_fin :
                    overlap =self.env['session.session'].search([
                    ('id', '!=', session.id),
                    ('candidat_ids' ,'in',session.candidat_ids.ids),
                    ('date_debut','<=', session.date_fin),
                    ('date_fin','>=', session.date_debut)
                    ])
                    if overlap:
                        listcandidats = [candidate.name for candidate in session.candidat_ids if
                                     candidate.id in overlap.mapped('candidat_ids').ids]
                        if listcandidats:
                            raise ValidationError('The following candidates are already assigned to another training on these days: {}'.format(
                                ', '.join(listcandidats)))


    @api.constrains('salle_ids', 'date_debut', 'date_fin')
    def room_available(self):
        for session in self:
            if session.salle_ids and session.date_debut and session.date_fin :
                search =self.env['session.session'].search([
                ('id', '!=', session.id),
                ('salle_ids' ,'in',session.salle_ids.ids),
                ('date_debut','<=', session.date_fin),
                ('date_fin','>=', session.date_debut)
                ])
                if search :
                    raise ValidationError('Room not available before session start!')

    @api.depends('salle_ids', 'date_debut', 'date_fin')
    def room_free_state(self):
        for session in self:
            current_date = fields.Datetime.now()
            if session.salle_ids:

                date_debut = fields.Datetime.from_string(session.date_debut)
                date_fin = fields.Datetime.from_string(session.date_fin)
                if  current_date >= date_debut and current_date <= date_fin:
                    session.salle_ids.Free = False
                else : session.salle_ids.Free= True
                # for salle in session.salle_ids:
                #     if date_debut <= current_date <= date_fin:
                #         salle.free = False
                #     else:
                #         salle.free = True


    @api.constrains('nb_participants_max')
    def _check_nb_participants_max(self):
        for session in self:
            if session.nb_participants_max <= 0:
                raise ValidationError("The maximum number of participants must be greater than 0.")
    def resev_button(self):
        candidate_id = 6
        for session in self:
            if session.nb_participants >= session.nb_participants_max:
                raise ValidationError("No place available!")

            elif candidate_id in session.candidat_ids.ids:
                raise ValidationError("Candidate already assigned to this session")

            else:
                session.nb_participants += 1
                session.candidat_ids = [(4, candidate_id)]









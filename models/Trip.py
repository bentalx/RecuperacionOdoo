from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class Trip(models.Model):
    _name = 'naturalparks.trip'
    _order = 'starting_date'

    name = fields.Char(string="name of the trip", required=True)
    trip_type = fields.Selection([('car', 'Car'), ('walking', 'Walking')]) 
    starting_date = fields.Datetime(required=True)
    ending_date = fields.Datetime(required=True)

    natural_park_id = fields.Many2one('naturalparks.natural_park', ondelete='cascade', string="Natural Park", required=True)
    lodging_id = fields.Many2one('naturalparks.lodging', string="lodging responsible", required=True)
    visitor_ids = fields.Many2many('naturalparks.visitor', string="Visitors")
    state = fields.Selection([
            ('1.draft', 'Draft'),
            ('2.confirm', 'Confirm'),
            ('3.done', 'Done'),
        ], string='Status', default='1.draft')

    @api.constrains('natural_park_id', 'visitor_ids')
    def _check_visitors(self):
        for r in self:
            if r.visitor_ids.natural_park_id != r.natural_park_id and len(r.visitor_ids) > 0:
                raise exceptions.ValidationError("error")

    @api.constrains('starting_date', 'ending_date')
    def _check_ending_date_is_after_starting_date(self):
        for r in self:
            if r.starting_date > r.ending_date:
                raise exceptions.ValidationError("error")
   
                
    def action_confirm(self):
        for r in self:
            r.state = '2.confirm'
            
    def action_done(self):
        for r in self:
            r.state = '3.done'

    def action_draft(self):
        for r in self:
            r.state = '1.draft'
    
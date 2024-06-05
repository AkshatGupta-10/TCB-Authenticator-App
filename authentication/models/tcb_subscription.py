import secrets
import string
from odoo import models, fields, api
from datetime import date, timedelta


class TCBSubscription(models.Model):
    _name = 'tcb.subscription'
    _description = 'TCB Subscription Details'


    client_id = fields.Char(string="Client ID",)
    client_secret = fields.Char(string="Client Secret")
    duration = fields.Integer(string="Duration (minutes)")
    key = fields.Char(string="Key")

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    validity = fields.Integer(string="Validity (Days)", default=30)


    def action_update_client_login(self):
        print("running")
        pass

    def action_generate_new_key(self):
        alphabet = string.ascii_letters + string.digits
        self.key = ''.join(secrets.choice(alphabet) for i in range(12))
        self.start_date = date.today()
        self._compute_end_date() 


    @api.depends("start_date", "validity")
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.validity:
                record.end_date = record.start_date + timedelta(days=record.validity)
            else:
                record.end_date = False
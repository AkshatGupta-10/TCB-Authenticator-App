# import secrets
# import string
from odoo.http import request
from odoo import models, fields, api
from datetime import date, timedelta
import uuid


class AuthenticatorApp(models.Model):
    _name = 'authenticator.app'
    _description = 'Authenticator App'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    client_url = fields.Char(string='Client URL', required=True)
    client_id = fields.Char(string="Client ID",)
    client_secret = fields.Char(string="Client Secret")
    duration = fields.Integer(string="Duration (minutes)")
    key = fields.Char(string="Key")
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ], default='draft', string='Stage')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ], default='draft', string='Status')

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    validity_days = fields.Integer(string="Validity (Days)", default=30)
    status_display = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ], compute='_compute_status_display', string='Status')


    @api.depends('start_date', 'validity_days')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + timedelta(days=record.validity_days)
            else:
                record.end_date = False

    @api.onchange('end_date')
    def _onchange_status(self):
        for record in self:
            if record.end_date and date.today() > record.end_date:
                record.status = 'expired'
            elif record.status != 'active':
                record.status = 'draft'

    @api.depends('status', 'end_date')
    def _compute_status_display(self):
        for record in self:
            if record.status == 'active':
                record.status_display = 'active'
            elif record.status == 'draft':
                record.status_display = 'draft'
            elif record.end_date and date.today() > record.end_date:
                record.status_display = 'expired'


    def action_generate_new_key(self):
        self.key = str(uuid.uuid4())
        self.stage = 'submitted'


    def action_update_client_login(self):
        self.start_date = date.today()
        self._compute_end_date() 
        self.status = 'active'



        # data_to_send = {
        # 'key': self.key,
        # 'end_date': self.end_date,
        # }
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # url = f"{base_url}/api/get_new_key" 

        # response = request.post(url, json=data_to_send)



















##############################-----------------############

    # @api.multi
    # def generate_key_and_submit(self):
    #     # Generate a random key
    #     self.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    #     self.stage = 'submitted'
    #     self.status = 'draft'
    #     self.start_date = fields.Date.context_today(self)
    #     self.end_date = self.start_date + timedelta(days=self.validity_days)
    #     # Make fields readonly
    #     self.write({'stage': 'submitted', 'start_date': self.start_date, 'end_date': self.end_date})
    
    # @api.multi
    # def update_in_client_system(self):
    #     for record in self:
    #         # Logic to call the client's URL with the key and validity
    #         # This can be implemented using the requests library to make an API call
    #         pass





    # @api.depends('start_date', 'validity_days')
    # def _compute_end_date(self):
    #     for rec in self:
    #         if rec.start_date:
    #             rec.end_date = rec.start_date + timedelta(days=rec.validity_days)

    # def action_generate_new_key(self):
    #     self.key = str(uuid.uuid4())  
    #     self.stage = 'submitted'
    #     # Make fields read-only here (e.g., using a custom access rule)
    #     self.env['ir.rule'].clear_caches()  # Clear rule cache to immediately enforce the new rule

    # # Define the access rule method
    # @api.model
    # def _tcb_subscription_is_readonly(self):
    #     """Custom access rule to make fields read-only when the stage is 'submitted'."""
    #     return self.stage == 'submitted'

    # def action_update_client_login(self):
    #     try:
    #         payload = {
    #             'key': self.key,
    #             'validity_days': self.validity_days
    #         }
    #         headers = {'Content-Type': 'application/json'}
    #         response = requests.post(self.client_url, json=payload, headers=headers)
    #         if response.status_code == 200:  # Successful update
    #             self.status = 'active'
    #             self.start_date = fields.Date.today()  # Set start date on successful update
    #     except requests.exceptions.RequestException as e:
    #         # Handle API call errors (e.g., log, show a message)
    #         pass

    # def action_update_client_login(self):
    #     print("running")
    #     pass

    # def action_generate_new_key(self):
    #     alphabet = string.ascii_letters + string.digits
    #     self.key = ''.join(secrets.choice(alphabet) for i in range(12))
    #     self.start_date = date.today()
    #     self._compute_end_date() 


    # @api.depends("start_date", "validity")
    # def _compute_end_date(self):
    #     for record in self:
    #         if record.start_date and record.validity:
    #             record.end_date = record.start_date + timedelta(days=record.validity)
    #         else:
    #             record.end_date = False
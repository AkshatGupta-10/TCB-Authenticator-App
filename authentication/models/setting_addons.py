from odoo import models, fields, api
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'


    key = fields.Char(string="Key", config_parameter='authentication.key')
    validity = fields.Datetime(string="Validity", invisible=True, config_parameter='authentication.validity')


    @api.onchange('key')
    def _onchange_key(self):
        """Update validity based on matching key from authenticator.app model."""
        if self.key:
            auth_app = self.env['authenticator.app'].search([('key', '=', self.key)], limit=1)
            if auth_app:
                self.validity = auth_app.end_date
            else:
                raise UserError(_("No matching key found in Authenticator App model."))


# 

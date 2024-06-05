import logging
import requests
from odoo import api, http, SUPERUSER_ID, _
from odoo.http import request


_logger = logging.getLogger(__name__)


class OAuthController(http.Controller):

    @http.route('/api/get_new_key', type='json', auth='public', csrf=False)
    def get_new_key(self, **kwargs):
        data = request.get_json_data()
        client_url = data.get('client_url', kwargs.get('client_url'))
        
        fields = ['key', 'end_date']
        print("Fields ==========" , fields)
        authenticator = request.env['authenticator.app'].sudo().search_read([('client_url', '=', client_url)],fields , limit=1)
        
        print("authenticator ---", authenticator)

        return authenticator


        # try:
        #     response = requests.post(external_portal_endpoint, json=data)
        #     response.raise_for_status()
        #     _logger.info("Data sent to external portal successfully")
        # except requests.RequestException as e:
        #     _logger.error(f"Error sending data to external portal: {e}")
        #     return Response(json.dumps({'error': str(e)}), status=500)

        # return Response(json.dumps({'message': 'Data sent successfully'}), status=200)/
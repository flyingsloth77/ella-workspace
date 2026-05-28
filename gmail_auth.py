#!/usr/bin/env python3
"""Gmail OAuth2 setup script - local server flow."""

import os
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
]

CLIENT_SECRET = '/root/.openclaw/media/inbound/client_secret_1042492627745_bcv2sp6gbujvmdv4cdh1etdd9u820nmn---4086c528-109c-49f7-aba2-d7aeb5f5552e.json'
TOKEN_PATH = '/root/.openclaw/workspace/gmail_token.json'

def main():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRET,
                scopes=SCOPES,
                redirect_uri='http://localhost:8080/'
            )
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
            print(f'\nOpen this URL in your browser:\n\n{auth_url}\n')
            print('Waiting for you to authorize... (listening on http://localhost:8080)')

            # Start local server to capture the redirect
            from http.server import HTTPServer, BaseHTTPRequestHandler
            from urllib.parse import urlparse, parse_qs

            auth_code = [None]

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self):
                    params = parse_qs(urlparse(self.path).query)
                    if 'code' in params:
                        auth_code[0] = params['code'][0]
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'<h1>Authorization successful! You can close this tab.</h1>')
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b'<h1>Error: no code received</h1>')

                def log_message(self, format, *args):
                    pass  # suppress logs

            server = HTTPServer(('localhost', 8080), Handler)
            server.handle_request()

            if not auth_code[0]:
                print('ERROR: No authorization code received.')
                return

            flow.fetch_token(code=auth_code[0])
            creds = flow.credentials

        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
        print(f'Token saved to {TOKEN_PATH}')

    print('Authentication successful!')

if __name__ == '__main__':
    main()

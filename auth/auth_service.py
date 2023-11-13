# Import necessary libraries
import os
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# OAuth 2.0 configuration
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

SERVER_HOST = os.getenv("SERVER_HOST")

# Create a Flask app
app = flask.Flask(__name__)
app.secret_key = 'supersecretkey1234'  # Replace with a secret key

# OAuth flow and authorization endpoint
@app.route('/get_token', methods=['GET'])
def get_token():
    # Check if the client already has valid credentials
    if 'credentials' in flask.session:
        credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
    else:
        # Create an OAuth flow
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES)
        flow.redirect_uri = "http://localhost/auth/oauth2callback" 
        # Generate the authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        flask.session['state'] = state

        return flask.redirect(authorization_url)

    # Return the access token
    return flask.jsonify({'access_token': credentials.token})

# OAuth callback endpoint
@app.route('/oauth2callback')
def oauth2callback():

    # Create an OAuth flow and handle the authorization response
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = "http://localhost/auth/oauth2callback"
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    # Redirect to the endpoint that returns the token
    return flask.redirect('http://localhost/protected')

# Helper function to convert credentials to a dictionary
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Disable in production
    app.run('localhost', 5000, debug=True)

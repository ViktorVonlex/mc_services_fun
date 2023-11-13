import os
import flask
import requests

app = flask.Flask(__name__)
app.secret_key = 'supersecretkey1234'  # Replace with a secure secret key

# The URL of the OAuth microservice to obtain a token
AUTH_HOST = os.getenv("AUTH_HOST")
# OAUTH_SERVICE_URL = 'http://' + AUTH_HOST + ':5000/get_token'
OAUTH_SERVICE_URL = 'http://localhost/auth/get_token'


# Index page available to everyone
@app.route('/')
def index():
    return 'Welcome to the Main App! <a href="/protected">Go to Protected Page</a>'

# Protected page that requires authentication
@app.route('/protected')
def protected():
    # Check if the user has a valid token in the session
    placeholder = flask.session
    print(placeholder)
    if 'credentials' in flask.session:
        return 'This is a protected page. You are authenticated!'
    else:
        # If the user is not authenticated, redirect to the OAuth microservice to obtain a token
        return flask.redirect(OAUTH_SERVICE_URL)
        response = requests.get(OAUTH_SERVICE_URL, allow_redirects=True)
        print(response.status_code)
        if response.status_code == 200:
            auth_url = response.json().get('auth_url')
            return flask.redirect(auth_url)
            # access_token = response.json().get('access_token')
            # flask.session['access_token'] = access_token
        else:
            return 'Authentication failed. Please try again or login to access this page.'

# Logout route to clear the session
@app.route('/logout')
def logout():
    if 'credentials' in flask.session:
        del flask.session['credentials']
        print(flask.session)
    return 'You have been logged out.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)


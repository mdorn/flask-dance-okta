import os

from flask import Flask, redirect, url_for, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', '$3cr3t')

issuer_url = '{}/v1'.format(os.environ.get('OKTA_ISSUER_URL'))
okta_blueprint = OAuth2ConsumerBlueprint(
    'okta', __name__,
    client_id=os.environ.get('OKTA_CLIENT_ID'),
    client_secret=os.environ.get('OKTA_CLIENT_SECRET'),
    base_url=issuer_url,
    token_url='{}/token'.format(issuer_url),
    authorization_url='{}/authorize'.format(issuer_url),
    scope=['openid', 'profile', 'email'],
    state=os.environ.get('OKTA_STATE')  # allow shared state with widget; normally this is dynamically generated
    # redirect_url='http://localhost:5000/other',
)
app.register_blueprint(okta_blueprint, url_prefix='/login')

@app.route('/')
def index():
    if not okta_blueprint.session.token:
        return redirect(url_for('okta.login'))
    resp = okta_blueprint.session.get('{}/userinfo'.format(issuer_url))
    msg = '<p>You are {email} on Okta. Access token:</p>'.format(email=resp.json()['email'])
    token_msg = '<pre style="white-space: pre-wrap;">{token}</pre>'.format(token=okta_blueprint.session.token['access_token'])
    return '{}{}'.format(msg, token_msg)


@app.route('/widget')
def widget():
    config = {
        'base_url': os.environ.get('OKTA_BASE_URL'),
        'issuer_url': os.environ.get('OKTA_ISSUER_URL'),
        'client_id': os.environ.get('OKTA_CLIENT_ID'),
        'state': os.environ.get('OKTA_STATE'),
    }
    return render_template('widget.html', config=config)

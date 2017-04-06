from time import time

from github_webhook import Webhook
from flask import Flask

# Setup
from os.path import exists
app = Flask(__name__)
github_secret = None
webhook = Webhook(app, '/postreceive', github_secret)


# Views
@app.route("/")
def index():
    return "Hello, World!"


@app.route("/healthcheck")
def healthcheck():
    return "GOOD"


@webhook.hook('push')
def on_push(data):
    """Handle a webhook from github.
    """
    timestamp = time()
    if exists('/srv/qmk_bot/received_hooks'):
        open('/srv/qmk_bot/received_hooks/%s.repr' % timestamp, 'w').write(repr(data))
        open('/srv/qmk_bot/received_hooks/%s.str' % timestamp, 'w').write(str(data))

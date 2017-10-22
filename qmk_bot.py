from flask import Flask
from github_webhook import Webhook
from update_kb_redis import update_kb_redis


# Setup
app = Flask(__name__)
app.config.from_object(__name__)
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
    print('Got webhook request:')
    print(data)
    print('Enqueing update:')
    print(job = update_kb_redis.delay())

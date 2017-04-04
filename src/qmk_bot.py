from github_webhook import Webhook
from flask import Flask

# Setup
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
    print("Got push with: {0}".format(data))

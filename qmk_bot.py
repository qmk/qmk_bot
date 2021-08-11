from pprint import pprint

from flask import Flask
from github_webhook import Webhook

from qmk_commands import discord_msg
from update_kb_redis import update_needed


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
    #pprint(data)
    if data['ref'] == 'refs/heads/master' and data['repository']['full_name'] in ['qmk/qmk_firmware', 'qmk/chibios', 'qmk/chibios-contrib']:
        print('Triggering update.')
        num_commits = len(data['commits'])
        name = data['pusher']['name']
        repo = data['repository']['full_name']
        new_hash=data['after']
        forced = 'force ' if data['forced'] else ''

        discord_msg('info', '%s has %spushed %s commits to %s. Head is now %s. Changes: %s' % (name, forced, num_commits, repo, new_hash, data['compare']))

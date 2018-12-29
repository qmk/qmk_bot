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
    print(data)
    if data['ref'] == 'refs/heads/master' and data['repository']['full_name'] in ['qmk/qmk_firmware', 'qmk/chibios', 'qmk/chibios-contrib']:
        print('Triggering update.')
        num_commits = len(data['commits'])
        name = data['pusher']['name']
        repo = data['repository']['full_name']
        old_hash=data['before']
        new_hash=data['after']
        commit_url = data['head_commit']['url']
        forced = 'force ' if data['forced'] else ''

        print(update_needed.delay(repo=repo, old_hash=old_hash, new_hash=new_hash))
        discord_msg('info', '%s has %spushed %s commits to %s. Head is now %s.' % (name, forced, num_commits, commit_url, new_hash))

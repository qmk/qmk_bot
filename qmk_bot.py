from pprint import pprint

from flask import Flask
from github_webhook import Webhook

import discord

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
    """Handle a push webhook from github.
    """
    print('Got push webhook request')
    if data['ref'] == 'refs/heads/master' and data['repository']['full_name'] in ['qmk/qmk_firmware', 'qmk/chibios', 'qmk/chibios-contrib']:
        print('Posting Discord message')
        num_commits = len(data['commits'])
        name = data['pusher']['name']
        repo = data['repository']['full_name']
        new_hash = data['after']
        forced = 'force ' if data['forced'] else ''

        discord.message('info', '%s has %spushed %s commits to %s. Head is now %s. Changes: %s' % (name, forced, num_commits, repo, new_hash, data['compare']))


@webhook.hook('workflow_run')
def on_workflow_run(data):
    """Handle a workflow_run webhook from github.
    """
    print('Got workflow_run webhook request')
    if data['action'] == 'completed':
        workflow = data['workflow']
        workflow_run = data['workflow_run']
        if workflow_run.get('conclusion') == 'failure':
            if workflow['name'] == 'Update develop after master merge':
                print('Posting Discord message: failed master -> develop merge')
                discord.message('error', '`master` -> `develop` merge failed! Run: %s' % (workflow_run['html_url']))
            elif workflow['name'] == 'Update API Data':
                branch = workflow_run['head_branch']
                print('Posting Discord message: failed API data update (%s)' % (branch))
                discord.message('error', 'API data update failed for branch %s' % (branch))

import hashlib
import hmac
import os

import git
from flask import Flask, render_template, request

app = Flask(__name__)


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


@app.route("/")
def default():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(err):
    return render_template("404.html", err=err)


@app.route('/update_server', methods=['POST'])
def webhook():
    repo_url = 'https://github.com/jeffykle/jeffkelly-dev-flask/settings/hooks'
    x_hub_signature = request.headers.get('X-Hub-Signature')
    w_secret = os.getenv('POST_MERGE_SECRET')

    if is_valid_signature(x_hub_signature, request.data, w_secret):
        if request.method == 'POST':
            repo = git.Repo('../')
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400
    else:
        return 'Unauthorized secret value.', 401


if __name__ == '__main__':
    app.run(debug=True)

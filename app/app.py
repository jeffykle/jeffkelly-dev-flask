import git
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def default():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(err):
    return render_template("404.html", err=err)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/jeffykle/jeffkelly-dev-flask/settings/hooks')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True)

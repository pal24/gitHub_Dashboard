from flask import Flask, render_template
from config import REPOS
from github_api import get_workflow_metadata

app = Flask(__name__)

@app.route("/")
def dashboard():
    results = [get_workflow_metadata(repo) for repo in REPOS]
    return render_template("dashboard.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

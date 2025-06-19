import requests
from config import GITHUB_TOKEN, WORKFLOW_FILE_NAME

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_workflow_metadata(repo):
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW_FILE_NAME}/runs?per_page=1"
    resp = requests.get(url, headers=HEADERS)
    
    if resp.status_code != 200:
        return {"repo": repo, "error": f"GitHub API error: {resp.status_code}"}

    data = resp.json()
    if "workflow_runs" in data and data["workflow_runs"]:
        run = data["workflow_runs"][0]
        return {
            "repo": repo,
            "status": run["status"],
            "conclusion": run["conclusion"],
            "timestamp": run["run_started_at"],
            "commit_message": run["head_commit"]["message"] if run.get("head_commit") else "N/A",
            "triggered_by": run["triggering_actor"]["login"] if run.get("triggering_actor") else "N/A"
        }
    return {"repo": repo, "error": "No workflow runs found"}

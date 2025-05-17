from github import Github
import os

def create_pr(repo_name, branch_name, title, body):
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_user().get_repo(repo_name)

    # Assumes you already pushed the branch
    pr = repo.create_pull(
        title=title,
        body=body,
        head=branch_name,
        base=\"main\"
    )
    print(f\"🔗 PR created: {pr.html_url}\")
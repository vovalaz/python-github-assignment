import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from github import Github

load_dotenv(find_dotenv())
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")


if __name__ == "__main__":
    if ACCESS_TOKEN:
        g = Github(ACCESS_TOKEN)
    else:
        g = Github()

    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    pull_requests = repo.get_pulls(state="open")

    for pr in pull_requests:
        print(f"Pull request #{pr.number}: {pr.title}")
        print(f"\tAuthor: {pr.user.login}")
        print(f"\tDate opened: {pr.created_at}")
        print(f"\tLast updated: {pr.updated_at}")
        print(f"\tURL: {pr.html_url}")
        print()

        print("Commits:")
        commits = pr.get_commits()
        for commit in commits:
            print(f"- {commit.sha} ({commit.committer.login})")
            print(f"  Message: {commit.commit.message}")
            print(f"  Date: {commit.commit.committer.date}")
            print(f"  URL: {commit.html_url}")
            print()

        print("Review comments:")
        review_comments = pr.get_review_comments()
        for comment in review_comments:
            print(f"- {comment.user.login}: {comment.body}")
            print(f"  Date: {comment.created_at}")
            print(f"  URL: {comment.html_url}")
            print()

        print("Requested reviewers:")
        requested_reviewers = pr.get_review_requests()
        for reviewer in requested_reviewers:
            print(f"- {reviewer.login}")
        print()

        now = datetime.utcnow()
        time_open = now - pr.created_at
        print(f"Time open: {time_open}\n")

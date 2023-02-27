import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from github import Github


if find_dotenv():
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

        print("\tCommits:")
        commits = pr.get_commits()
        for commit in commits:
            print(f"\t\t- {commit.sha} ({commit.committer.login})")
            print(f"\t\tMessage: {commit.commit.message}")
            print(f"\t\tDate: {commit.commit.committer.date}")
            print(f"\t\tURL: {commit.html_url}")
            print()

        print("\tComments:")
        comments = pr.get_issue_comments()
        for comment in comments:
            print(f"\t\t- {comment.user.login}: {comment.body}")
            print(f"\t\tDate: {comment.created_at}")
            print(f"\t\tURL: {comment.html_url}")
            print()

        print("\tReviewers:")
        requested_reviewers, requested_reviewers_team = pr.get_review_requests()
        for reviewer in requested_reviewers:
            print(f"\t\t- {reviewer.login}")
        print()

        now = datetime.utcnow()
        time_open = now - pr.created_at
        print(f"\tTime open: {time_open}\n")
        print("------------------------------------------------------------------------------------------")
        print()

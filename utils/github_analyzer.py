from github import Github
from datetime import datetime
import os


def analyze_repo(repo_url):
    """
    Analyzes a GitHub repository and returns repository info and file list
    """

    # ✅ Clean URL
    repo_url = repo_url.strip()
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]

    # ✅ Extract owner and repo safely
    try:
        _, _, _, owner, repo_name = repo_url.split("/", 4)
    except ValueError:
        raise ValueError("Invalid GitHub repository URL format")

    # ✅ Authenticate GitHub client
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)

    # ✅ Fetch repository
    try:
        repo = g.get_repo(f"{owner}/{repo_name}")
    except Exception as e:
        print("GITHUB ERROR >>>", e)
        raise ValueError("Unable to access repository")

    # ✅ Collect all files
    files = []
    contents = repo.get_contents("")
    while contents:
        item = contents.pop(0)
        if item.type == "dir":
            try:
                contents.extend(repo.get_contents(item.path))
            except Exception:
                continue
        else:
            files.append(item.path)

    # ✅ Format dates
    created_at = repo.created_at.strftime("%b %d, %Y") if repo.created_at else "N/A"
    updated_at = repo.updated_at.strftime("%b %d, %Y") if repo.updated_at else "N/A"

    # ✅ Repository info
    repo_info = {
        "name": repo.full_name,
        "description": repo.description,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "watchers": repo.watchers_count,
        "open_issues": repo.open_issues_count,
        "language": repo.language,
        "size": repo.size,
        "created_at": created_at,
        "updated_at": updated_at,
        "license": repo.license.name if repo.license else None,
        "topics": repo.get_topics() if hasattr(repo, "get_topics") else [],
        "avatar_url": repo.owner.avatar_url if repo.owner else None,
        "default_branch": repo.default_branch,
        "has_wiki": repo.has_wiki,
        "has_issues": repo.has_issues,
        "has_projects": repo.has_projects,
    }

    return repo_info, files


# ✅ ADDED FUNCTION (ONLY ADDITION)
def get_file_content(repo, path):
    """
    Fetch and return decoded content of a file from GitHub repository
    """
    file = repo.get_contents(path)
    return file.decoded_content.decode("utf-8", errors="ignore")

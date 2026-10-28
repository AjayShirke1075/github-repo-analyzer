"""
GitHub Repository Analyzer
Fetches repository metadata, file trees, and source code using PyGithub.
Optimized for rate limits with Git Tree API and multi-tier authentication fallback.
"""

from github import Github, Auth, GithubException
import os
from typing import Tuple, List, Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def get_github_client(token: Optional[str] = None) -> Github:
    """
    Creates an authenticated or anonymous Github client.
    Tests credentials safely and falls back to anonymous if invalid.
    """
    active_token = token or os.getenv("GITHUB_TOKEN")
    
    if active_token and len(active_token.strip()) > 10 and not active_token.startswith("ghp_YOUR"):
        try:
            client = Github(auth=Auth.Token(active_token.strip()))
            # Light validation
            _ = client.get_user().login
            return client
        except GithubException as e:
            if e.status == 401:
                print("[GitHub Notice] Configured token invalid or expired; falling back to anonymous access.")
            else:
                print(f"[GitHub Notice] Auth warning: {e}; falling back to anonymous access.")
        except Exception:
            pass

    return Github()


def fetch_file_content(repo: Any, file_path: str, max_chars: int = 5000) -> str:
    """
    Safely retrieves text content of a file from the repository.
    """
    try:
        content_file = repo.get_contents(file_path)
        raw_bytes = content_file.decoded_content
        text = raw_bytes.decode("utf-8", errors="replace")
        return text[:max_chars]
    except Exception as e:
        print(f"[GitHub Notice] Could not read {file_path}: {e}")
        return ""


def analyze_repo(repo_url: str, custom_token: Optional[str] = None) -> Tuple[Dict[str, Any], List[str], Any]:
    """
    Analyzes a GitHub repository and returns (repo_info, files, repo_object).
    Uses Git Tree API to fetch the entire repository file tree in 1 request.
    """
    # Clean URL
    clean_url = repo_url.strip().rstrip("/")
    if "github.com/" not in clean_url:
        raise ValueError("Please provide a valid GitHub repository URL (e.g. https://github.com/owner/repo).")

    # Extract owner and repo safely
    try:
        parts = clean_url.split("github.com/")[1].split("/")
        owner, repo_name = parts[0], parts[1]
    except Exception:
        raise ValueError("Invalid GitHub repository URL format. Expected: https://github.com/owner/repo")

    repo_full_name = f"{owner}/{repo_name}"
    g = get_github_client(custom_token)

    try:
        repo = g.get_repo(repo_full_name)
    except GithubException as e:
        if e.status == 404:
            raise ValueError(f"Repository '{repo_full_name}' was not found. Please ensure it is public and spelled correctly.") from e
        elif e.status == 403:
            raise ValueError("GitHub API rate limit reached. Please wait a short while or provide a personal access token.") from e
        elif e.status == 401:
            # Fallback to pure anonymous client
            g = Github()
            try:
                repo = g.get_repo(repo_full_name)
            except Exception as e2:
                raise ValueError("Unable to access repository. It may be private or inaccessible.") from e2
        else:
            raise ValueError(f"GitHub access error: {e.data.get('message', str(e))}") from e
    except Exception as e:
        raise ValueError(f"Failed to connect to GitHub: {str(e)}") from e

    # Fetch file list efficiently via Git Tree (1 API call!)
    files: List[str] = []
    try:
        default_branch = repo.default_branch or "main"
        tree = repo.get_git_tree(default_branch, recursive=True)
        files = [item.path for item in tree.tree if item.type == "blob"]
    except Exception as e:
        print(f"[GitHub Tree Notice] Falling back to recursive get_contents: {e}")
        try:
            contents = repo.get_contents("")
            count = 0
            while contents and count < 200:
                item = contents.pop(0)
                count += 1
                if item.type == "dir":
                    try:
                        contents.extend(repo.get_contents(item.path))
                    except Exception:
                        continue
                else:
                    files.append(item.path)
        except Exception as e2:
            print(f"[GitHub Notice] Contents fallback error: {e2}")

    # Format dates
    created_at = repo.created_at.strftime("%b %d, %Y") if repo.created_at else "N/A"
    updated_at = repo.updated_at.strftime("%b %d, %Y") if repo.updated_at else "N/A"

    repo_info = {
        "name": repo.full_name,
        "description": repo.description or "No description provided",
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "watchers": repo.watchers_count,
        "open_issues": repo.open_issues_count,
        "language": repo.language or "Multi-language",
        "size": repo.size,
        "created_at": created_at,
        "updated_at": updated_at,
        "license": repo.license.name if repo.license else "No License",
        "topics": repo.get_topics() if hasattr(repo, "get_topics") else [],
        "avatar_url": repo.owner.avatar_url if repo.owner else None,
        "default_branch": repo.default_branch or "main",
        "has_wiki": repo.has_wiki,
        "has_issues": repo.has_issues,
        "has_projects": repo.has_projects,
    }

    return repo_info, files, repo

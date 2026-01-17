"""GitHub integration tool for repository analysis and operations."""
import os
from typing import Any

import httpx


async def github_repo_info(owner: str, repo: str) -> dict[str, Any]:
    """
    Get information about a GitHub repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        
    Returns:
        Dictionary with repository information or error
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "error": f"Repository {owner}/{repo} not found"
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Set GITHUB_TOKEN to increase limits."
                }
            elif response.status_code != 200:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}"
                }
                
            data = response.json()
            
            return {
                "success": True,
                "result": {
                    "name": data["name"],
                    "full_name": data["full_name"],
                    "description": data.get("description", "No description"),
                    "owner": data["owner"]["login"],
                    "stars": data["stargazers_count"],
                    "forks": data["forks_count"],
                    "open_issues": data["open_issues_count"],
                    "language": data.get("language", "Unknown"),
                    "default_branch": data["default_branch"],
                    "created_at": data["created_at"],
                    "updated_at": data["updated_at"],
                    "topics": data.get("topics", []),
                    "license": data["license"]["name"] if data.get("license") else None,
                    "homepage": data.get("homepage"),
                    "html_url": data["html_url"]
                },
                "details": {
                    "owner": owner,
                    "repo": repo
                }
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timeout while connecting to GitHub API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching repository info: {str(e)}"
        }


async def github_search_repos(query: str, max_results: int = 5) -> dict[str, Any]:
    """
    Search for GitHub repositories.
    
    Args:
        query: Search query (e.g., "machine learning python")
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Dictionary with search results or error
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "per_page": min(max_results, 30), "sort": "stars"},
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Set GITHUB_TOKEN to increase limits."
                }
            elif response.status_code != 200:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}"
                }
                
            data = response.json()
            
            results = []
            for item in data.get("items", [])[:max_results]:
                results.append({
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "description": item.get("description", "No description"),
                    "stars": item["stargazers_count"],
                    "language": item.get("language", "Unknown"),
                    "html_url": item["html_url"]
                })
            
            return {
                "success": True,
                "result": results,
                "details": {
                    "query": query,
                    "total_count": data["total_count"],
                    "returned": len(results)
                }
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timeout while connecting to GitHub API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching repositories: {str(e)}"
        }


async def github_list_issues(
    owner: str,
    repo: str,
    state: str = "open",
    max_results: int = 10
) -> dict[str, Any]:
    """
    List issues for a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state - 'open', 'closed', or 'all' (default: 'open')
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        Dictionary with issues list or error
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/issues",
                params={"state": state, "per_page": min(max_results, 30)},
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "error": f"Repository {owner}/{repo} not found"
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Set GITHUB_TOKEN to increase limits."
                }
            elif response.status_code != 200:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}"
                }
                
            data = response.json()
            
            issues = []
            for item in data[:max_results]:
                # Skip pull requests (they appear in issues endpoint)
                if "pull_request" in item:
                    continue
                    
                issues.append({
                    "number": item["number"],
                    "title": item["title"],
                    "state": item["state"],
                    "author": item["user"]["login"],
                    "labels": [label["name"] for label in item.get("labels", [])],
                    "created_at": item["created_at"],
                    "updated_at": item["updated_at"],
                    "comments": item["comments"],
                    "html_url": item["html_url"]
                })
            
            return {
                "success": True,
                "result": issues,
                "details": {
                    "owner": owner,
                    "repo": repo,
                    "state": state,
                    "count": len(issues)
                }
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timeout while connecting to GitHub API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing issues: {str(e)}"
        }


async def github_repo_languages(owner: str, repo: str) -> dict[str, Any]:
    """
    Get programming languages used in a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        Dictionary with language statistics or error
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/languages",
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "error": f"Repository {owner}/{repo} not found"
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Set GITHUB_TOKEN to increase limits."
                }
            elif response.status_code != 200:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}"
                }
                
            data = response.json()
            
            # Calculate total bytes
            total_bytes = sum(data.values())
            
            # Calculate percentages
            languages = []
            for lang, bytes_count in sorted(data.items(), key=lambda x: x[1], reverse=True):
                percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
                languages.append({
                    "language": lang,
                    "bytes": bytes_count,
                    "percentage": round(percentage, 2)
                })
            
            return {
                "success": True,
                "result": languages,
                "details": {
                    "owner": owner,
                    "repo": repo,
                    "total_bytes": total_bytes,
                    "language_count": len(languages)
                }
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timeout while connecting to GitHub API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching languages: {str(e)}"
        }

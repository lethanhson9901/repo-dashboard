import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv(Path(__file__).parent.parent / '.env')

def get_env_var(var_name, fallback_var_name=None):
    """
    Get environment variable with fallback name support.
    This allows support for both local dev (GITHUB_*) and CI (GH_*) environment variables.
    """
    value = os.getenv(var_name)
    if not value and fallback_var_name:
        value = os.getenv(fallback_var_name)
    return value

def get_starred_repos():
    """
    Fetch basic information about starred repositories.
    Uses environment variables for configuration.
    """
    # Try both GITHUB_USERNAME and GH_USERNAME
    github_username = get_env_var('GITHUB_USERNAME', 'GH_USERNAME')
    token = get_env_var('GITHUB_TOKEN', 'GH_PAT')
    
    if not github_username:
        raise ValueError("GitHub username not found in environment variables (GITHUB_USERNAME or GH_USERNAME)")
    
    base_url = f"https://api.github.com/users/{github_username}/starred"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    starred_repos = []
    page = 1
    per_page = int(os.getenv('ITEMS_PER_PAGE', 100))
    api_version = os.getenv('GITHUB_API_VERSION')
    
    if api_version:
        headers["X-GitHub-Api-Version"] = api_version
    
    while True:
        params = {
            "page": page,
            "per_page": per_page
        }
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            
            repos = response.json()
            if not repos:
                break
                
            for repo in repos:
                repo_info = {
                    "name": repo["full_name"],
                    "description": repo["description"],
                    "url": repo["html_url"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"],
                    "last_updated": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "owner": {
                        "username": repo["owner"]["login"],
                        "profile_url": repo["owner"]["html_url"]
                    }
                }
                starred_repos.append(repo_info)
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
            
    return starred_repos

def save_to_file(repos):
    """Save the repositories data to a JSON file"""
    output_file = os.getenv('OUTPUT_FILE', 'starred_repos.json')
    
    # Create the directory structure if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2)

def print_summary(repos):
    """Print a basic summary of the repositories"""
    print(f"\nFound {len(repos)} starred repositories")
    
    # Language statistics
    languages = {}
    for repo in repos:
        lang = repo["language"] or "Unknown"
        languages[lang] = languages.get(lang, 0) + 1
    
    print("\nTop Programming Languages:")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{lang}: {count}")

if __name__ == "__main__":
    repos = get_starred_repos()
    save_to_file(repos)
    print_summary(repos)
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_starred_repos():
    """
    Fetch basic information about starred repositories.
    Uses environment variables for configuration.
    """
    github_username = os.getenv('GITHUB_USERNAME')
    token = os.getenv('GITHUB_TOKEN')
    
    if not github_username:
        raise ValueError("GITHUB_USERNAME not found in environment variables")
    
    base_url = f"https://api.github.com/users/{github_username}/starred"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    starred_repos = []
    page = 1
    
    while True:
        params = {
            "page": page,
            "per_page": 100
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
    with open(output_file, "w", encoding="utf-8") as f:
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
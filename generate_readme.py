#!/usr/bin/env python3
import datetime
import requests
import os
import json
from collections import Counter

# GitHub username
USERNAME = "nikita20002000"

# Default user information - will be updated with GitHub API data
USER_INFO = {
    "name": "Nikita Novikov",
    "title": "Software Developer",
    "location": "Russia",
    "email": "novikov.nikita.work@yandex.ru",
    "website": f"https://github.com/{USERNAME}",
    "lang": ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#"],
    "social": {
        "GitHub": f"https://github.com/{USERNAME}",
        "Telegram": "@nikita_vse_po_plany"
    },
    # GitHub information for neofetch style - will be populated from API
    "github": {
        "profile": f"https://github.com/{USERNAME}",
        "repositories": "Loading...",
        "followers": "Loading...",
        "following": "Loading...",
        "contributions": "Loading...",
        "stars": "Loading...",
        "forks": "Loading...",
        "issues": "Loading...",
        "pull_requests": "Loading...",
        "languages": "Loading...",
        "top_language": "Loading...",
        "second_language": "Loading...",
        "third_language": "Loading...",
        "joined": "Loading...",
        "activity": "Loading...",
        "streak": "Loading...",
        "longest_streak": "Loading...",
        "organizations": "Loading...",
        "gists": "Loading...",
        "sponsors": "Loading...",
        "achievements": "Loading...",
        "projects": "Loading..."
    }
}

def get_github_token():
    """Get GitHub token from environment variable"""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN environment variable not set. Using limited API access.")
    return token

def fetch_github_data():
    """Fetch GitHub data using the GitHub API"""
    token = get_github_token()
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    # Base API URL
    api_url = "https://api.github.com"

    try:
        # Fetch user profile data
        user_response = requests.get(f"{api_url}/users/{USERNAME}", headers=headers)
        user_data = user_response.json()

        if user_response.status_code != 200:
            print(f"Error fetching user data: {user_data.get('message', 'Unknown error')}")
            return

        # Update basic user info
        USER_INFO["name"] = user_data.get("name", USER_INFO["name"])
        USER_INFO["github"]["profile"] = user_data.get("html_url", USER_INFO["github"]["profile"])
        USER_INFO["github"]["followers"] = str(user_data.get("followers", 0))
        USER_INFO["github"]["following"] = str(user_data.get("following", 0))
        USER_INFO["github"]["joined"] = user_data.get("created_at", "").split("T")[0] if user_data.get("created_at") else "Unknown"

        # Fetch repositories
        repos_response = requests.get(f"{api_url}/users/{USERNAME}/repos?per_page=100", headers=headers)
        repos_data = repos_response.json()

        if repos_response.status_code != 200:
            print(f"Error fetching repos data: {repos_data.get('message', 'Unknown error')}")
        else:
            # Count repositories
            USER_INFO["github"]["repositories"] = f"{len(repos_data)} public repositories"

            # Count stars, forks, and collect languages
            stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
            forks = sum(repo.get("forks_count", 0) for repo in repos_data)
            USER_INFO["github"]["stars"] = f"{stars} received"
            USER_INFO["github"]["forks"] = f"{forks} received"

            # Collect languages
            languages = []
            for repo in repos_data:
                if repo.get("language") and repo.get("language") not in languages:
                    languages.append(repo.get("language"))

            USER_INFO["github"]["languages"] = ", ".join(languages[:4])

            # Get language statistics
            language_counts = Counter()
            for repo in repos_data:
                if repo.get("language"):
                    # Weight by stars + 1 to give some importance to popular repos
                    language_counts[repo.get("language")] += repo.get("stargazers_count", 0) + 1

            # Get top 3 languages
            top_languages = language_counts.most_common(3)
            if top_languages:
                total = sum(count for lang, count in top_languages)
                if len(top_languages) >= 1:
                    lang, count = top_languages[0]
                    percentage = int((count / total) * 100)
                    USER_INFO["github"]["top_language"] = f"{lang} ({percentage}%)"
                if len(top_languages) >= 2:
                    lang, count = top_languages[1]
                    percentage = int((count / total) * 100)
                    USER_INFO["github"]["second_language"] = f"{lang} ({percentage}%)"
                if len(top_languages) >= 3:
                    lang, count = top_languages[2]
                    percentage = int((count / total) * 100)
                    USER_INFO["github"]["third_language"] = f"{lang} ({percentage}%)"

        # Fetch organizations
        orgs_response = requests.get(f"{api_url}/users/{USERNAME}/orgs", headers=headers)
        orgs_data = orgs_response.json()

        if orgs_response.status_code != 200:
            print(f"Error fetching orgs data: {orgs_data.get('message', 'Unknown error')}")
        else:
            USER_INFO["github"]["organizations"] = f"Member of {len(orgs_data)} organizations"

        # Fetch gists
        gists_response = requests.get(f"{api_url}/users/{USERNAME}/gists", headers=headers)
        gists_data = gists_response.json()

        if gists_response.status_code != 200:
            print(f"Error fetching gists data: {gists_data.get('message', 'Unknown error')}")
        else:
            USER_INFO["github"]["gists"] = f"{len(gists_data)} public gists"

        # Set some values that can't be easily determined from the API
        USER_INFO["github"]["activity"] = "Active" if len(repos_data) > 0 else "Inactive"
        USER_INFO["github"]["contributions"] = "Check profile for contributions"
        USER_INFO["github"]["issues"] = "Check profile for issues"
        USER_INFO["github"]["pull_requests"] = "Check profile for PRs"
        USER_INFO["github"]["streak"] = "Check profile for streak"
        USER_INFO["github"]["longest_streak"] = "Check profile for longest streak"
        USER_INFO["github"]["sponsors"] = "Open to sponsorship"
        USER_INFO["github"]["achievements"] = "Check profile for achievements"
        USER_INFO["github"]["projects"] = f"{min(5, len(repos_data))} pinned projects"

        print("GitHub data fetched successfully!")

    except Exception as e:
        print(f"Error fetching GitHub data: {str(e)}")

def generate_arch_logo():
    """Generate ASCII art for Arch Linux logo"""
    return """\
                    -`
                   .o+`
                  `ooo/
                 `+oooo:
                `+oooooo:
                -+oooooo+:
              `/:-:++oooo+:
             `/++++/+++++++:
            `/++++++++++++++:
           `/+++ooooooooooooo/`
          ./ooosssso++osssssso+`
         .oossssso-````/ossssss+`
        -osssssso.      :ssssssso.
       :osssssss/        osssso+++.
      /ossssssss/        +ssssooo/-
    `/ossssso+/:-        -:/+osssso+-
   `+sso+:-`                 `.-/+oso:
  `++:.                           `-/+/
  .`                                 `/
"""

def generate_prompt():
    """Generate a terminal-like prompt"""
    return f"{USERNAME}@github:~$ "

def generate_command(cmd):
    """Format a command with the prompt"""
    return f"{generate_prompt()}{cmd}\n"

def generate_output(output, indent=2):
    """Format command output with indentation"""
    indent_str = " " * indent
    if isinstance(output, list):
        return "\n".join(f"{indent_str}{item}" for item in output)
    else:
        return f"{indent_str}{output}"

def format_terminal_line(content, total_width=72):
    """Format a line to fit within the terminal borders with proper spacing"""
    content_width = len(content)
    padding = total_width - content_width - 4  # 4 for "│ " at start and " │" at end
    return f"│ {content}{' ' * padding} │"

def generate_neofetch_github_section():
    """Generate the neofetch-style section with user and GitHub information"""
    now = datetime.datetime.now()

    # Get the Arch Linux logo
    logo_lines = generate_arch_logo().strip().split('\n')

    # Prepare GitHub information lines
    github_info = [
        f"{USERNAME}@github",
        "-------------------------------",
        f"Profile: {USER_INFO['github']['profile']}",
        f"Repositories: {USER_INFO['github']['repositories']}",
        f"Followers: {USER_INFO['github']['followers']}",
        f"Following: {USER_INFO['github']['following']}",
        f"Contributions: {USER_INFO['github']['contributions']}",
        f"Stars: {USER_INFO['github']['stars']}",
        f"Forks: {USER_INFO['github']['forks']}",
        f"Issues: {USER_INFO['github']['issues']}",
        f"Pull Requests: {USER_INFO['github']['pull_requests']}",
        f"Languages: {USER_INFO['github']['languages']}",
        f"Top Language: {USER_INFO['github']['top_language']}",
        f"Second Language: {USER_INFO['github']['second_language']}",
        f"Third Language: {USER_INFO['github']['third_language']}",
        f"Joined: {USER_INFO['github']['joined']}",
        f"Activity: {USER_INFO['github']['activity']}",
        f"Streak: {USER_INFO['github']['streak']}",
        f"Longest Streak: {USER_INFO['github']['longest_streak']}",
        f"Organizations: {USER_INFO['github']['organizations']}",
        f"Gists: {USER_INFO['github']['gists']}",
        f"Sponsors: {USER_INFO['github']['sponsors']}",
        f"Achievements: {USER_INFO['github']['achievements']}",
        f"Projects: {USER_INFO['github']['projects']}"
    ]

    # Calculate the fixed width for the logo section to ensure consistent alignment
    # Add a bit more space (40) to ensure good separation between logo and info
    logo_width = 40

    combined_lines = []

    # Ensure both lists have the same length by padding the shorter one
    max_lines = max(len(logo_lines), len(github_info))
    if len(logo_lines) < max_lines:
        logo_lines.extend([''] * (max_lines - len(logo_lines)))
    if len(github_info) < max_lines:
        github_info.extend([''] * (max_lines - len(github_info)))

    # Combine the lines with fixed-width spacing
    for i in range(max_lines):
        logo_line = logo_lines[i] if i < len(logo_lines) else ''
        info_line = github_info[i] if i < len(github_info) else ''

        # Format with fixed width for consistent alignment
        formatted_line = f"{logo_line:{logo_width}}{info_line}"
        combined_lines.append(formatted_line)

    return '\n'.join(combined_lines)

def generate_github_stats():
    """Generate the GitHub stats widgets section"""
    return f"""
<div align="center">

[![Trophies](https://github-profile-trophy.vercel.app/?username={USERNAME}&theme=onedark)](https://github.com/ryo-ma/github-profile-trophy)

</div>
"""

def generate_readme():
    """Generate the complete README.md content"""
    sections = [
        "# " + USER_INFO["name"] + " - " + USER_INFO["title"],
        "",
        "<div>",
        "",
        "```",
        generate_neofetch_github_section(),
        "```",
        "",
        "</div>",
        "",
        generate_github_stats(),
        "",
        "<div align='center'>",
        f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "</div>"
    ]

    return "\n".join(sections)

def main():
    """Main function to generate and save the README.md file"""
    # Fetch the latest GitHub data
    fetch_github_data()

    # Generate README content with the updated data
    readme_content = generate_readme()

    with open("README.md", "w") as f:
        f.write(readme_content)

    print(f"README.md has been generated successfully!")

if __name__ == "__main__":
    main()

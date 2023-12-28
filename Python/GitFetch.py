import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import webbrowser

def get_github_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    try:
        response = requests.get(url)
        response.raise_for_status()
        repositories = response.json()
        return repositories
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

def get_repository_details(username, repo_name):
    url = f'https://api.github.com/repos/{username}/{repo_name}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        repository = response.json()
        return repository
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

def display_repository_info(repo_text, repository):
    repo_text.insert(tk.END, f"\nRepository: {repository['name']}\n", "bold")
    repo_text.insert(tk.END, f"Description: {repository['description']}\n")
    repo_text.insert(tk.END, f"URL: {repository['html_url']}\n")
    repo_text.insert(tk.END, f"Stars: {repository['stargazers_count']} | ")
    repo_text.insert(tk.END, f"Forks: {repository['forks_count']} | ")
    repo_text.insert(tk.END, f"Watchers: {repository['watchers_count']} | ")
    repo_text.insert(tk.END, f"Last Updated: {repository['updated_at']}\n\n")

def display_detailed_info(repo_text, repository):
    contributors_url = repository['contributors_url']
    contributors_response = requests.get(contributors_url)
    
    if contributors_response.status_code == 200:
        contributors = contributors_response.json()
        repo_text.insert(tk.END, "Contributors:\n", "bold")
        for contributor in contributors:
            repo_text.insert(tk.END, f"  - {contributor['login']}\n")
        repo_text.insert(tk.END, "\n")

    issues_url = repository['issues_url'].replace("{/number}", "")
    issues_response = requests.get(issues_url)
    
    if issues_response.status_code == 200:
        issues = issues_response.json()
        repo_text.insert(tk.END, "Open Issues:\n", "bold")
        for issue in issues:
            repo_text.insert(tk.END, f"  - {issue['title']} ({issue['html_url']})\n")
        repo_text.insert(tk.END, "\n")

    releases_url = repository['releases_url'].replace("{/id}", "")
    releases_response = requests.get(releases_url)
    
    if releases_response.status_code == 200:
        releases = releases_response.json()
        repo_text.insert(tk.END, "Releases:\n", "bold")
        for release in releases:
            repo_text.insert(tk.END, f"  - {release['name']} ({release['html_url']})\n")
        repo_text.insert(tk.END, "\n")

    repo_text.insert(tk.END, f"Language: {repository['language']}\n")
    repo_text.insert(tk.END, f"Default Branch: {repository['default_branch']}\n")
    repo_text.insert(tk.END, f"Clone URL: {repository['clone_url']}\n")
    repo_text.insert(tk.END, f"SSH URL: {repository['ssh_url']}\n")
    repo_text.insert(tk.END, f"HTTPS URL: {repository['html_url']}.git\n")
    repo_text.insert(tk.END, f"License: {repository['license']['name'] if repository['license'] else 'N/A'}\n")
    repo_text.insert(tk.END, f"File Size: {repository['size']} KB\n")
    repo_text.insert(tk.END, f"File Count: {repository['size']}\n")
    repo_text.insert(tk.END, f"Created At: {repository['created_at']}\n")
    repo_text.insert(tk.END, f"Updated At: {repository['updated_at']}\n")
    repo_text.insert(tk.END, f"Pushed At: {repository['pushed_at']}\n")

    repo_text.insert(tk.END, "\n")

def open_url(url):
    webbrowser.open_new(url)

def fetch_data(username_entry, repo_text):
    username = username_entry.get()
    
    if not username:
        repo_text.config(state=tk.NORMAL)
        repo_text.delete(1.0, tk.END)
        repo_text.insert(tk.END, "Please enter a GitHub username.")
        repo_text.config(state=tk.DISABLED)
        return
    
    repo_text.config(state=tk.NORMAL)
    repo_text.delete(1.0, tk.END)
    repo_text.insert(tk.END, f"Fetching repositories for {username}...\n", "italic")
    repo_text.config(state=tk.DISABLED)

    repositories = get_github_repositories(username)

    if repositories:
        repo_text.config(state=tk.NORMAL)
        repo_text.delete(1.0, tk.END)
        repo_text.insert(tk.END, f"Repositories for {username}:\n", "bold")
        
        for repo in repositories:
            display_repository_info(repo_text, repo)
            repo_text.insert(tk.END, "Fetching detailed information...\n", "italic")
            detailed_repo = get_repository_details(username, repo['name'])
            if detailed_repo:
                display_detailed_info(repo_text, detailed_repo)
        
        repo_text.config(state=tk.DISABLED)
    else:
        repo_text.config(state=tk.NORMAL)
        repo_text.delete(1.0, tk.END)
        repo_text.insert(tk.END, "Failed to fetch repositories. Please try again.", "error")
        repo_text.config(state=tk.DISABLED)

def on_search(username_entry, repo_text):
    thread = threading.Thread(target=fetch_data, args=(username_entry, repo_text))
    thread.start()

def main():
    window = tk.Tk()
    window.title("GitFetch by LiamDevelopz")
    window.geometry("900x700")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TText", font=("Courier New", 10))

    username_label = ttk.Label(window, text="Enter GitHub username:")
    username_label.pack(pady=5)

    username_entry = ttk.Entry(window, font=("Arial", 12))
    username_entry.pack(pady=5)

    search_button = ttk.Button(window, text="Search", command=lambda: on_search(username_entry, repo_text))
    search_button.pack(pady=5)

    repo_text = scrolledtext.ScrolledText(window, width=100, height=30, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10))
    repo_text.pack(pady=10)

    link_tags = ["bold", "italic", "error"]
    for tag in link_tags:
        repo_text.tag_configure(tag, foreground="blue", underline=True)
        repo_text.tag_bind(tag, "<Button-1>", lambda event, tag=tag: open_url(repo_text.get(tk.SEL_FIRST, tk.SEL_LAST)) if repo_text.tag_ranges(tk.SEL) else None)

    window.mainloop()

if __name__ == "__main__":
    main()

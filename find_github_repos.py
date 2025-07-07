import os
import subprocess

def find_git_repos(start_path):
    matches = []
    for root, dirs, files in os.walk(start_path):
        if '.git' in dirs:
            matches.append(root)
            dirs.remove('.git')  # Skip descending into .git folder
    return matches

def get_github_remote(repo_path):
    try:
        remotes = subprocess.check_output(
            ['git', '-C', repo_path, 'remote', '-v'],
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in remotes.splitlines():
            if 'github.com' in line:
                return line.split()[1]
    except subprocess.CalledProcessError:
        pass
    return None

if __name__ == '__main__':
    start_path = os.path.expanduser("~")  # start from home directory
    print(f"Scanning for Git repos under: {start_path}\n")
    repos = find_git_repos(start_path)
    found = 0
    for repo in repos:
        remote = get_github_remote(repo)
        if remote:
            found += 1
            print(f"[{found}] {repo}")
            print(f"    → {remote}\n")
    if found == 0:
        print("No GitHub-connected repos found.")   
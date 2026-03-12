#!/usr/bin/env python3
import os
import json
import subprocess
import requests
from datetime import datetime

# ------------------------
# Config
# ------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Set this in Codespace secrets
GITHUB_REPO = "dainantonio/repo-guardian"  # Replace with your GitHub repo path
BASE_BRANCH = "main"
BOT_BRANCH = "repo-guardian-auto"

# ------------------------
# Helper functions
# ------------------------
def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

def create_branch(branch):
    stdout, _ = run_cmd(["git", "checkout", "-B", branch])
    return stdout

def commit_changes():
    run_cmd(["git", "add", "."])
    run_cmd(["git", "commit", "-m", "🤖 Repo Guardian: auto-cleanup & scan"])
    run_cmd(["git", "push", "-u", "origin", BOT_BRANCH])

# ------------------------
# GitHub PR
# ------------------------
def create_pr(title, body):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "head": BOT_BRANCH,
        "base": BASE_BRANCH,
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        pr_url = response.json().get("html_url")
        print(f"✅ PR created: {pr_url}")
        return pr_url
    else:
        print(f"❌ PR creation failed: {response.text}")
        return None

def post_pr_comment(pr_number, comment):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    requests.post(url, headers=headers, json=data)

# ------------------------
# Scan functions
# ------------------------
def find_console_logs():
    issues = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines):
                        if "console.log" in line:
                            issues.append(f"{path}:{i+1}")
                except:
                    pass
    return issues

def find_large_files(max_lines=300):
    large_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".jsx", ".ts", ".tsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        line_count = len(f.readlines())
                    if line_count > max_lines:
                        large_files.append(f"{path} ({line_count} lines)")
                except:
                    pass
    return large_files

def find_empty_files():
    empty_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)
            try:
                if os.path.getsize(path) == 0:
                    empty_files.append(path)
            except:
                pass
    return empty_files

def find_unused_files():
    unused = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx", ".py")):
                path = os.path.join(root, file)
                try:
                    if os.path.getsize(path) < 50:
                        unused.append(path)
                except:
                    pass
    return unused

def find_unused_dependencies():
    unused = []
    # JS dependencies
    if os.path.exists("package.json"):
        try:
            with open("package.json") as f:
                pkg = json.load(f)
            deps = pkg.get("dependencies", {})
            for dep in deps:
                found = False
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                            path = os.path.join(root, file)
                            with open(path, "r", encoding="utf-8") as f2:
                                if dep in f2.read():
                                    found = True
                                    break
                    if found: break
                if not found:
                    unused.append(f"JS: {dep}")
        except:
            pass
    # Python dependencies
    if os.path.exists("requirements.txt"):
        try:
            with open("requirements.txt") as f:
                reqs = f.readlines()
            for req in reqs:
                pkg_name = req.strip().split("==")[0]
                found = False
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if file.endswith(".py"):
                            path = os.path.join(root, file)
                            with open(path, "r", encoding="utf-8") as f2:
                                if pkg_name in f2.read():
                                    found = True
                                    break
                    if found: break
                if not found:
                    unused.append(f"PY: {pkg_name}")
        except:
            pass
    return unused

# ------------------------
# Health score
# ------------------------
def calculate_health(logs, large_files, empty_files, unused_files, unused_deps):
    score = 100
    score -= min(len(logs)*3,30)
    score -= min(len(large_files)*2,20)
    score -= min(len(empty_files)*2,10)
    score -= min(len(unused_files)*1,10)
    score -= min(len(unused_deps)*2,20)
    return max(score,0)

# ------------------------
# Run full scan & create PR
# ------------------------
def run_repo_guardian():
    print("🔍 Scanning repo...")

    logs = find_console_logs()
    large_files = find_large_files()
    empty_files = find_empty_files()
    unused_files = find_unused_files()
    unused_deps = find_unused_dependencies()

    # Remove console logs
    for f in logs:
        file_path = f.split(":")[0]
        try:
            with open(file_path, "r") as fp:
                lines = fp.readlines()
            lines = [line for line in lines if "console.log" not in line]
            with open(file_path, "w") as fp:
                fp.writelines(lines)
        except: pass

    # Commit & push branch
    create_branch(BOT_BRANCH)
    commit_changes()

    score = calculate_health(logs, large_files, empty_files, unused_files, unused_deps)

    # Generate PR body
    body = f"## Repo Guardian Scan Results\n\n"
    body += f"**Repo Health Score:** {score}/100\n\n"
    def fmt_list(items, desc):
        return "\n".join(f"- {i}" for i in items) if items else f"✅ No {desc} found."
    body += "### Console Logs Removed\n" + fmt_list(logs, "console logs") + "\n\n"
    body += "### Large Files\n" + fmt_list(large_files, "large files") + "\n\n"
    body += "### Empty Files\n" + fmt_list(empty_files, "empty files") + "\n\n"
    body += "### Potentially Unused Files\n" + fmt_list(unused_files, "unused files") + "\n\n"
    body += "### Unused Dependencies\n" + fmt_list(unused_deps, "unused dependencies") + "\n\n"

    pr_url = create_pr(title="🤖 Repo Guardian Auto PR", body=body)
    print(f"🎉 Scan complete. PR ready at {pr_url}")

# ------------------------
# Entry
# ------------------------
if __name__ == "__main__":
    run_repo_guardian()
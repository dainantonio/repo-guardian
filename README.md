# Repo Guardian: Autonomous Repo Butler 🤖💼

Repo Guardian is an autonomous GitHub agent that scans your repository, removes console logs, identifies large, empty, or unused files, detects unused dependencies, calculates a **Repo Health Score**, and automatically creates a **Pull Request** with a full report.

---

## Features

- 🔍 **Repo Scanning**
  - Finds and removes `console.log` statements in JS/TS files.
  - Detects large files (>300 lines by default), empty files, and potentially unused files.
  - Detects unused JS and Python dependencies.

- 🛠 **Automatic Cleanup**
  - Removes console logs automatically.
  - Commits changes to a new branch.

- 📊 **Repo Health Score**
  - Calculates a score from 0–100 based on console logs, large files, empty files, unused files, and dependencies.

- 📄 **Pull Request Creation**
  - Automatically creates a PR on GitHub with a Markdown report of all findings.
  - Provides clear summary of repo health and issues.

- ⚡ **Ready for Expansion**
  - Can be upgraded to comment on individual lines in PRs like a code reviewer.
  - Can run periodically or on-demand for continuous repo maintenance.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dainantonio/repo-guardian.git
cd repo-guardian


2. Create a GitHub Personal Access Token (PAT)

Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token.

Give it a name: Repo Guardian Bot.

Set expiration (optional).

Scope: repo (full control of private repos) or public_repo for public repos.

Copy the token.

3. Set the Token in Codespaces (or locally)

Temporary (current terminal session):

export GITHUB_TOKEN="ghp_your_token_here"

Persistent (every Codespaces session):
Add the line to ~/.bashrc or ~/.zshrc:

export GITHUB_TOKEN="ghp_your_token_here"

Reload shell:

source ~/.bashrc   # or source ~/.zshrc
4. Configure the Repository in agent.py
GITHUB_REPO = "dainantonio/repo-guardian"  # Replace with your GitHub username/repo
BASE_BRANCH = "main"
BOT_BRANCH = "repo-guardian-auto"
Usage

Run the agent to scan and clean your repo:

python3 agent.py

The agent will:

Create the branch repo-guardian-auto

Scan the repository for console logs, large/empty/unused files, and unused dependencies

Remove console logs automatically

Commit the changes

Push the branch to GitHub

Create a Pull Request with a Markdown report and Repo Health Score

Example PR Report
## Repo Guardian Scan Results

**Repo Health Score:** 92/100

### Console Logs Removed
- src/app.js:23
- src/utils/logger.js:10

### Large Files
- src/components/BigComponent.jsx (450 lines)

### Empty Files
✅ No empty files found.

### Potentially Unused Files
- src/old_module.js

### Unused Dependencies
- JS: lodash
- PY: requests
Troubleshooting

PR Creation Failed (404):
Ensure GITHUB_REPO is correct (username/repo-name) and the token has repo scope.
Make sure your branch exists remotely (git push -u origin repo-guardian-auto).

Token Not Found:
Make sure GITHUB_TOKEN is exported in your shell or Codespace.

Python Errors:
Ensure Python 3.8+ is installed and required modules exist:

pip install requests
Future Enhancements

Line-by-line PR comments like a code reviewer

Periodic scans with GitHub Actions

Integration with ESLint/Pylint for auto-fixes

Continuous repo health monitoring in CI/CD

License

MIT License © Dain Antonio


---

This version is **clear, concise, and user-friendly**, perfect for your repo homepage.  

If you want, I can also **create a small workflow diagram** for the README showing:  

`Scan → Cleanup → Commit → Push → PR → Report`  

It’ll make it visually appealing.  

Do you want me to do that next?

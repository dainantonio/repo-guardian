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

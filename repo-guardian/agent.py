#!/usr/bin/env python3
import os
import yaml
import subprocess
import json
from datetime import datetime

# ------------------------
# Helper functions
# ------------------------
def load_rules():
    try:
        with open("cleanup_rules.yaml", "r") as f:
            return yaml.safe_load(f)
    except:
        return {}

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
                            issues.append((path, i + 1))
                except:
                    pass
    return issues

def remove_console_logs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        cleaned = [line for line in lines if "console.log" not in line]
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cleaned)
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

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
                        large_files.append((path, line_count))
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

    # JS/Node
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
                if not found: unused.append(f"JS: {dep}")
        except:
            pass

    # Python
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
                if not found: unused.append(f"PY: {pkg_name}")
        except:
            pass

    return unused

def commit_changes(branch_name="repo-guardian-auto"):
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    except subprocess.CalledProcessError:
        # branch exists? just checkout
        subprocess.run(["git", "checkout", branch_name], check=True)

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "🤖 Repo Guardian: auto-cleanup & scan"], check=True
        )
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
        print(f"✅ Changes committed and pushed to branch '{branch_name}'!")
    except subprocess.CalledProcessError:
        print("ℹ️ No changes to commit.")

def calculate_health(logs, large_files, empty_files, unused_files, unused_deps):
    score = 100
    score -= min(len(logs) * 3, 30)
    score -= min(len(large_files) * 2, 20)
    score -= min(len(empty_files) * 2, 10)
    score -= min(len(unused_files) * 1, 10)
    score -= min(len(unused_deps) * 2, 20)
    return max(score, 0)

def generate_report(logs, large_files, empty_files, unused_files, unused_deps, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"# Repo Guardian Report — {timestamp}\n\n"
    report += f"**Repo Health Score:** {score}/100\n\n"

    def list_or_ok(items, desc):
        if items:
            return "\n".join([f"- {item}" for item in items])
        else:
            return f"✅ No {desc} found."

    report += "## Console Logs Removed\n"
    report += list_or_ok([f"{file}:{line}" for file, line in logs], "console logs") + "\n\n"
    report += "## Large Files\n"
    report += list_or_ok([f"{file} ({lines} lines)" for file, lines in large_files], "large files") + "\n\n"
    report += "## Empty Files\n"
    report += list_or_ok(empty_files, "empty files") + "\n\n"
    report += "## Potentially Unused Files\n"
    report += list_or_ok(unused_files, "unused files") + "\n\n"
    report += "## Unused Dependencies\n"
    report += list_or_ok(unused_deps, "unused dependencies") + "\n\n"

    with open("REPO_GUARDIAN_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("📝 Markdown report generated: REPO_GUARDIAN_REPORT.md")

# ------------------------
# Main Runner
# ------------------------
def run_cleanup():
    print("🔍 Scanning repo...\n")

    logs = find_console_logs()
    if logs:
        for file, line in logs:
            print(f"Cleaning console log in {file}")
            remove_console_logs(file)
    else:
        print("✅ No console logs found.")

    large_files = find_large_files()
    empty_files = find_empty_files()
    unused_files = find_unused_files()
    unused_deps = find_unused_dependencies()

    print("\n💾 Committing changes and creating branch...")
    commit_changes(branch_name="repo-guardian-auto")

    score = calculate_health(logs, large_files, empty_files, unused_files, unused_deps)
    print(f"\n📊 Repo Health Score: {score}/100")

    generate_report(logs, large_files, empty_files, unused_files, unused_deps, score)
    print("🎉 Repo scan complete! Ready for PR review.")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    run_cleanup()
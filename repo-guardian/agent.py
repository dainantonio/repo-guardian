#!/usr/bin/env python3
import os
import yaml
import subprocess

# ------------------------
# Load cleanup rules
# ------------------------
def load_rules():
    with open("cleanup_rules.yaml", "r") as f:
        return yaml.safe_load(f)

# ------------------------
# Find console.log statements
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
                            issues.append((path, i + 1))
                except:
                    pass
    return issues

# ------------------------
# Remove console.log from file
# ------------------------
def remove_console_logs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned = [line for line in lines if "console.log" not in line]

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cleaned)
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

# ------------------------
# Detect large files
# ------------------------
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

# ------------------------
# Detect empty files
# ------------------------
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

# ------------------------
# Git auto-commit
# ------------------------
def commit_changes():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "🤖 Repo Guardian: auto-cleanup and scan"], check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes committed and pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("ℹ️ No changes to commit.")

# ------------------------
# Main cleanup runner
# ------------------------
def run_cleanup():
    print("🔍 Scanning repo...\n")

    # 1️⃣ Console logs
    logs = find_console_logs()
    if logs:
        for file, line in logs:
            print(f"Cleaning console log in {file}")
            remove_console_logs(file)
    else:
        print("✅ No console logs found.")

    # 2️⃣ Large files
    print("\n📂 Checking for large files...")
    large_files = find_large_files()
    if large_files:
        for file, lines in large_files:
            print(f"⚠️ Large file detected: {file} ({lines} lines)")
    else:
        print("✅ No oversized files found.")

    # 3️⃣ Empty files
    print("\n🗑 Checking for empty files...")
    empty_files = find_empty_files()
    if empty_files:
        for file in empty_files:
            print(f"⚠️ Empty file detected: {file}")
    else:
        print("✅ No empty files found.")

    # 4️⃣ Commit any changes
    print("\n💾 Committing changes if any...")
    commit_changes()

    print("\n🎉 Repo scan complete!")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    run_cleanup()
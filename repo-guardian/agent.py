#!/usr/bin/env python3
import os
import yaml
import subprocess

# ------------------------
# Load cleanup rules
# ------------------------
def load_rules():
    try:
        with open("cleanup_rules.yaml", "r") as f:
            return yaml.safe_load(f)
    except:
        return {}

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
# Detect unused files (zero imports / very small JS/TS files)
# ------------------------
def find_unused_files():
    unused = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx", ".py")):
                path = os.path.join(root, file)
                try:
                    if os.path.getsize(path) < 50:  # small files might be unused
                        unused.append(path)
                except:
                    pass
    return unused

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
# Generate Repo Health Score
# ------------------------
def calculate_health(logs, large_files, empty_files, unused_files):
    score = 100
    score -= min(len(logs) * 3, 30)          # max penalty for logs
    score -= min(len(large_files) * 2, 20)   # max penalty for large files
    score -= min(len(empty_files) * 2, 10)   # max penalty for empty files
    score -= min(len(unused_files) * 1, 10)  # max penalty for unused files
    return max(score, 0)

# ------------------------
# Main runner
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

    # 4️⃣ Unused files
    print("\n📦 Checking for potentially unused files...")
    unused_files = find_unused_files()
    if unused_files:
        for file in unused_files:
            print(f"⚠️ Potential unused file: {file}")
    else:
        print("✅ No unused files found.")

    # 5️⃣ Commit changes
    print("\n💾 Committing changes if any...")
    commit_changes()

    # 6️⃣ Repo Health Score
    score = calculate_health(logs, large_files, empty_files, unused_files)
    print(f"\n📊 Repo Health Score: {score}/100")
    print("🎉 Repo scan complete!")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    run_cleanup()
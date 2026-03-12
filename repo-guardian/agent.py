import os
import yaml


def load_rules():
    with open("cleanup_rules.yaml", "r") as f:
        return yaml.safe_load(f)


def find_console_logs():
    issues = []

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".js") or file.endswith(".jsx"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    if "console.log" in line:
                        issues.append((path, i + 1))

    return issues


def remove_console_logs(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    cleaned = [line for line in lines if "console.log" not in line]

    with open(file_path, "w") as f:
        f.writelines(cleaned)


def run_cleanup():
    print("Scanning repo...")

    logs = find_console_logs()

    if len(logs) == 0:
        print("No console logs found.")
    else:
        for file, line in logs:
            print(f"Cleaning console log in {file}")
            remove_console_logs(file)


if __name__ == "__main__":
    run_cleanup()
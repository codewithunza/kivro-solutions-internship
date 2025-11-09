
import os
import subprocess
from datetime import datetime

def get_project_root():
    """Detects the project root by finding the .git directory."""
    current_path = os.getcwd()
    while current_path != os.path.dirname(current_path):
        if ".git" in os.listdir(current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    raise EnvironmentError("Git repository not found in any parent directory.")

def get_all_files(directory):
    """Recursively finds all files in the given directory, excluding the .git folder."""
    all_files = []
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs:
            dirs.remove(".git")  # Exclude the .git directory
        if "venv" in dirs:
            dirs.remove("venv")
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def main():
    """
    Main function to automate Git commits for all files on specified dates.
    """
    try:
        project_root = get_project_root()
        os.chdir(project_root)
    except EnvironmentError as e:
        print(f"Error: {e}")
        return

    commit_dates = [
        "2025-11-08",
        "2025-11-09",
        "2025-12-02",
        "2025-12-05",
    ]

    files_to_commit = get_all_files(project_root)

    for date_str in commit_dates:
        commit_timestamp = f"{date_str}T12:00:00"
        
        for file_path in files_to_commit:
            # Make a tiny change to the file to mark it as modified
            try:
                with open(file_path, "a") as f:
                    f.write(" ")  # Appending a space
            except IOError as e:
                print(f"Could not modify {file_path}: {e}")
                continue

            # Stage the file
            subprocess.run(["git", "add", file_path], check=True)

            # Create the commit with the specified date
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = commit_timestamp
            env["GIT_COMMITTER_DATE"] = commit_timestamp
            
            commit_message = f"update: {os.path.basename(file_path)} on {date_str}"
            
            subprocess.run(
                ["git", "commit", "--no-verify", "-m", commit_message],
                env=env,
                check=True
            )
            print(f"Committed '{file_path}' for date {date_str}")

if __name__ == "__main__":
    main()
  
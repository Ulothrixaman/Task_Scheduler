import subprocess

def automate_git(commit_message, repository_link):
    try:
        # Initialize the Git repository
        subprocess.run(['git', 'init'], check=True)

        # Add all files to staging area
        subprocess.run(['git', 'add', '.'], check=True)

        # Commit with the provided message
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        # Rename the branch to 'main' (assuming it's on a new repo)
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)

        # Add the remote repository
        subprocess.run(['git', 'remote', 'add', 'origin', repository_link], check=True)

        # Push the initial commit to the remote repository
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
# Example usage:
commit_msg = input("Enter commit message: ")
repo_link = input("Enter repository link: ")

automate_git(commit_msg, repo_link)

"""
Script Name         : update_all_submodules.py
Script Description  : Automates the process of updating all submodules within the 'embedded-linux' repository to the latest versions from their original repositories.

Author  : Omar Rizk
Course  : Python Programming
Diploma : Embedded Linux Diploma (Under Supervision of Eng. Moatasem Elsayed)
"""

import subprocess
import os

def run_command(command):
    """Run a shell command and print its output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}\n{err.decode().strip()}")
    else:
        print(out.decode().strip())
    return process.returncode, out.decode().strip(), err.decode().strip()

def update_all_submodules(repo_path, branch="main"):
    """Update all submodules to the latest commit."""
    os.chdir(repo_path)
    print(f"Changed directory to: {repo_path}")
    
    # Initialize and update all submodules
    run_command("git submodule init")
    run_command("git submodule update --remote --merge")
    
    # Get the list of submodules
    result = subprocess.run("git config --file .gitmodules --get-regexp path", shell=True, capture_output=True, text=True)
    submodules = [line.split()[1] for line in result.stdout.strip().split('\n')]
    
    for submodule in submodules:
        # Change to the submodule directory
        os.chdir(os.path.join(repo_path, submodule))
        print(f"Changed directory to submodule: {submodule}")
        
        # Fetch the latest changes and checkout the specified branch
        run_command("git fetch")
        run_command(f"git checkout {branch}")
        run_command(f"git pull origin {branch}")
        
        # Change back to the main repository directory
        os.chdir(repo_path)
        print(f"Changed directory back to: {repo_path}")
        
        # Stage the updated submodule
        run_command(f"git add {submodule}")
    
    # Check for changes before committing
    return_code, output, _ = run_command("git status --porcelain=v1")
    if not any(line.startswith(' M') for line in output.split('\n')):
        print("No changes to commit.")
    else:
        # Commit the changes
        commit_message = "Update all submodules to latest versions"
        run_command(f'git commit -m "{commit_message}"')
        
        # Push the changes to the remote repository
        run_command("git push origin main")

if __name__ == "__main__":
    # Define the path to your main repository
    embedded_linux_repo_path = "/home/rizk/Desktop/my-repos/embedded-linux-diploma"
    
    # Update all submodules
    update_all_submodules(embedded_linux_repo_path)

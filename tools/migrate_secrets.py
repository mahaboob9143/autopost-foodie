import os
import subprocess
import sys

def run_command(command):
    """Runs a shell command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        return None
    return result.stdout.strip()

def migrate_secrets(source_repo, target_repo, env_file=".env"):
    """
    Sets secrets in the target repository using values from a local .env file.
    Note: GitHub doesn't allow reading secret values, so we use the local .env as the source.
    """
    if not os.path.exists(env_file):
        print(f"Error: {env_file} not found.")
        return

    print(f"Migrating secrets to {target_repo} using {env_file}...")

    # Define which keys from .env should be uploaded as secrets
    secret_keys = [
        "META_ACCESS_TOKEN",
        "IG_ACCOUNT_ID",
        "FB_PAGE_ACCESS_TOKEN",
        "FB_PAGE_ID",
        "CLOUDINARY_CLOUD_NAME",
        "CLOUDINARY_API_KEY",
        "CLOUDINARY_API_SECRET",
        "CLOUDINARY_FOLDER",
        "IG_SESSION_ID",
        "IG_SCRAPE_USER",
        "YT_CLIENT_ID",
        "YT_CLIENT_SECRET",
        "YT_REFRESH_TOKEN"
    ]

    # Create a temporary secrets file for gh secret set -f
    temp_secrets_path = "temp_secrets.env"
    found_any = False
    
    with open(env_file, "r") as f:
        lines = f.readlines()
        
    with open(temp_secrets_path, "w") as f:
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                if key in secret_keys:
                    f.write(f"{key}={value}\n")
                    found_any = True

    if not found_any:
        print("No matching secrets found in .env file.")
        if os.path.exists(temp_secrets_path):
            os.remove(temp_secrets_path)
        return

    # Use gh CLI to set secrets from the file
    print(f"Setting secrets in {target_repo}...")
    cmd = f"gh secret set -f {temp_secrets_path} --repo {target_repo}"
    result = run_command(cmd)
    
    if result is not None:
        print("Secrets migrated successfully!")
    
    # Clean up
    if os.path.exists(temp_secrets_path):
        os.remove(temp_secrets_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/migrate_secrets.py <target_repo_handle>")
        print("Example: python tools/migrate_secrets.py mahaboob9143/autopost-foodie")
        sys.exit(1)

    target = sys.argv[1]
    migrate_secrets(None, target)

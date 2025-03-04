import argparse
import re
import subprocess

def extract_file_id(url):
    """Extracts the file ID from a Google Drive URL."""
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)

def download_file(file_id, filename):
    """Downloads a large file from Google Drive using curl, handling confirmation tokens."""
    
    # Step 1: Get initial response and extract confirmation token
    token_command = f'curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id={file_id}"'
    token_response = subprocess.getoutput(token_command)

    # Extract confirmation token
    token_match = re.search(r'confirm=([0-9A-Za-z_-]+)', token_response)
    token = token_match.group(1) if token_match else ""

    # Step 2: Check if a token was found
    if not token:
        print("❌ Error: Could not retrieve confirmation token. Trying without it...")
        token_param = ""
    else:
        token_param = f'&confirm={token}'

    # Step 3: Download the file
    download_command = f'curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download{token_param}&id={file_id}" -o "{filename}"'
    subprocess.run(download_command, shell=True)

    print(f"✅ Download complete: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Drive Large File Downloader")
    parser.add_argument("--url", required=True, help="Google Drive file URL")
    parser.add_argument("--save", required=True, help="Filename to save as")
    args = parser.parse_args()

    try:
        file_id = extract_file_id(args.url)
        download_file(file_id, args.save)
    except Exception as e:
        print(f"❌ Error: {e}")

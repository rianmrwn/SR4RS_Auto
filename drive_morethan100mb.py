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
    """Downloads a large file from Google Drive using curl."""
    
    # Step 1: Get confirmation token
    cmd_token = f'curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id={file_id}" | grep -o "confirm=[^&]*" | cut -d= -f2'
    token = subprocess.getoutput(cmd_token).strip()

    if not token:
        print("❌ Error: Could not retrieve confirmation token. Check your link.")
        return

    # Step 2: Download the file with the token
    download_cmd = f'curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm={token}&id={file_id}" -o "{filename}"'
    subprocess.run(download_cmd, shell=True)
    
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

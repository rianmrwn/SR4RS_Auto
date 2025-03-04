import argparse
import re
import requests

def extract_file_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)

def download_file(file_id, filename):
    session = requests.Session()
    base_url = "https://drive.google.com/uc?export=download"

    # Step 1: Get initial response to check for large file confirmation
    response = session.get(base_url, params={'id': file_id}, stream=True)
    
    # Step 2: Get the confirmation token if needed
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    # Step 3: If there is a token, make a second request with the token
    if token:
        response = session.get(base_url, params={'id': file_id, 'confirm': token}, stream=True)

    # Step 4: Download the file in chunks
    with open(filename, "wb") as f:
        for chunk in response.iter_content(32768):  # 32KB chunks
            if chunk:
                f.write(chunk)

    print(f"✅ Download complete: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Drive Downloader")
    parser.add_argument("--url", required=True, help="Google Drive file URL")
    parser.add_argument("--save", required=True, help="Filename to save as")
    args = parser.parse_args()

    file_id = extract_file_id(args.url)
    download_file(file_id, args.save)

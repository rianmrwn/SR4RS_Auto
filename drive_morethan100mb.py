import argparse
import re
import requests
import os

def extract_file_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def download_file(file_id, filename):
    session = requests.Session()
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = session.get(url, stream=True)
    token = get_confirm_token(response)

    if token:
        url = f"https://drive.google.com/uc?export=download"
        response = session.get(url, params={'id': file_id, 'confirm': token}, stream=True)

    with open(filename, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)
    
    print(f"Download complete: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Google Drive Downloader')
    parser.add_argument('--url', required=True, help='Google Drive file URL')
    parser.add_argument('--save', required=True, help='Filename to save as')
    args = parser.parse_args()

    file_id = extract_file_id(args.url)
    download_file(file_id, args.save)

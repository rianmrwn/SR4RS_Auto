import argparse
import re
import subprocess
import requests

def extract_file_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)

def download_file(file_id, filename):
    # First, retrieve the confirmation token for large files
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    session = requests.Session()
    
    # Initial request to get confirmation token
    response = session.get(download_url, stream=True)
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            # Get the confirmation token (Google uses the 'confirm' parameter to bypass virus scan)
            confirm_token = value
            download_url = f'https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}'
            break
    
    # Download the actual file with wget
    subprocess.run(['wget', '--no-check-certificate', download_url, '-O', filename])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Google Drive Downloader')
    parser.add_argument('--url', required=True, help='Google Drive file URL')
    parser.add_argument('--save', required=True, help='Filename to save as')
    args = parser.parse_args()

    file_id = extract_file_id(args.url)
    download_file(file_id, args.save)

import argparse
import re
import subprocess

def extract_file_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)

def download_file(file_id, filename):
    download_url = f'https://docs.google.com/uc?export=download&id={file_id}'
    subprocess.run(['wget', '--no-check-certificate', download_url, '-O', filename])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Google Drive Downloader')
    parser.add_argument('--url', required=True, help='Google Drive file URL')
    parser.add_argument('--save', required=True, help='Filename to save as')
    args = parser.parse_args()

    file_id = extract_file_id(args.url)
    download_file(file_id, args.save)
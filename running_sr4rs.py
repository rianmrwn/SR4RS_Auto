import argparse
import subprocess

def run_docker(device):
    if device == 'gpu':
        subprocess.run(['docker', 'run', '-ti', '--runtime=nvidia', 'mdl4eo/otbtf:3.4.0-gpu', 'bash'])
    else:
        subprocess.run(['docker', 'run', '-ti', '-v', '~/data:/mnt/data', 'mdl4eo/otbtf:3.4.0-cpu', 'bash'])

def download_and_unzip_model():
    subprocess.run(['wget', 'https://nextcloud.inrae.fr/s/boabW9yCjdpLPGX/download/sr4rs_sentinel2_bands4328_france2020_savedmodel.zip'])
    subprocess.run(['unzip', 'sr4rs_sentinel2_bands4328_france2020_savedmodel.zip'])

def clone_repo(git_url):
    subprocess.run(['git', 'clone', git_url])

def run_sr_script(input_file, output_file):
    subprocess.run(['python', 'sr4rs/code/sr.py', '--savedmodel', 'sr4rs_sentinel2_bands4328_france2020_savedmodel', '--input', input_file, '--output', output_file])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automate Docker and Python workflow')
    parser.add_argument('--device', required=True, choices=['gpu', 'cpu'], help='Device to use (gpu or cpu)')
    parser.add_argument('--giturl', required=True, help='Git repository URL')
    parser.add_argument('--load', required=True, help='Input file')
    parser.add_argument('--saving', required=True, help='Output file')
    args = parser.parse_args()

    run_docker(args.device)
    download_and_unzip_model()
    clone_repo(args.giturl)
    run_sr_script(args.load, args.saving)
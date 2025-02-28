import argparse
import subprocess

def download_and_unzip_model():
    subprocess.run(['wget', 'https://nextcloud.inrae.fr/s/boabW9yCjdpLPGX/download/sr4rs_sentinel2_bands4328_france2020_savedmodel.zip'])
    subprocess.run(['unzip', 'sr4rs_sentinel2_bands4328_france2020_savedmodel.zip'])

def run_sr_script(input_file, output_file):
    subprocess.run(['python', 'SR4RS_Auto/code/sr.py', '--savedmodel', 'sr4rs_sentinel2_bands4328_france2020_savedmodel', '--input', input_file, '--output', output_file])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automate Docker and Python workflow')
    parser.add_argument('--load', required=True, help='Input file')
    parser.add_argument('--saving', required=True, help='Output file')
    args = parser.parse_args()

    download_and_unzip_model()
    run_sr_script(args.load, args.saving)

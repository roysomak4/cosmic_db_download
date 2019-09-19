import argparse
import json
import requests
import sys
from os import environ
import sh


def main():
    # get input arguments for download link
    args = parse_input_args()
    download_url = args.download_url
    output_filename = download_url.split('/')[-1]

    # check if COSMIC login credentials ENV variable exists
    cosmic_db_creds = environ.get('COSMIC_DB_CREDS')
    if cosmic_db_creds == None:
        print('COSMIC database login credentials not found in this system. Please ensure that COSMIC_DB_CREDS environment variable exists.')
        print('Exiting program')
        sys.exit(1)
    
    # use the cosmic credentials to get the download link.
    print('Fetching authorized download link...')
    auth_download_link = get_cosmic_download_link(download_url, cosmic_db_creds)
    print('Got authorized download link.')

    # download the actual database file
    print('Downloading file from COSMIC...')
    sh.bash("-c", f"curl '{auth_download_link}' -o {output_filename}", _fg=True)
            

def get_cosmic_download_link(url, creds):
    headers = {'Authorization': f'Basic {creds}'}
    resp = requests.get(url, headers=headers)
    auth_download_link = json.loads(resp.text)['url']
    return auth_download_link


def parse_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('download_url',
                        type=str,
                        help='Cosmic database download url. Required field.')
    return parser.parse_args()


if __name__ == '__main__':
    main()

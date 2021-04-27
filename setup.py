import requests
import time
import zipfile
import os
import shutil
from os.path import join

#NOT WORKING YET

OUTPUT_PATH = 'GPT2-API/'
files_to_download = {
    1: {
        'name': 'models.zip',
        'url': 'http://170.253.56.17:8000/agatacloud/files/models.zip'
    }
}

class Downloader():

    def __init__(self, url, name):
        self.URL = url
        self.name = name
        self.destination = f'.temp/{name}'

    def download_file(self, chunk_size=32768):
        r = requests.get(self.URL, stream=True)
        if r.status_code == 200:
            with open(self.destination, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
    
    def unzip(self):
        with zipfile.ZipFile(self.destination, 'r') as zip_ref:
            zip_ref.extractall(f'{OUTPUT_PATH}')

if __name__ == '__main__':
    print('Preparing to download all necesary files...')

    if not os.path.exists('.temp/'):
        os.makedirs('.temp/')

    for file_to_download in files_to_download:
        file_name = files_to_download[file_to_download]['name']
        url_file = files_to_download[file_to_download]['url']
        print(f'Preparing to download {file_name}...')
        downloader = Downloader(url=url_file, name=file_name)
        downloader.download_file()
        print(f'{file_name} downloaded. Preparing extraction...')
        downloader.unzip()
        print(f'{file_name} extracted correctly.')

    shutil.rmtree('.temp/') #remove .temp/ folder to save space... If you want to conserve all raw zips delete this line or comment it.
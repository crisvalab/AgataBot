import requests
import time
import zipfile
import os
import shutil
from os.path import join

OUTPUT_PATH = 'GPT2-API/'
files_to_download = {
    1: {
        'id': '1ml2KHN3UHCI9PCu0iwlDdLa9TD6x6759',
        'name': 'models.zip',
        'url': 'https://drive.google.com/file/d/1ml2KHN3UHCI9PCu0iwlDdLa9TD6x6759/view?usp=sharing'
    },
    2: {
        'id': '1i6hPUrY-VSJCMXXu7hgdBW2stAhVuCbj',
        'name': 'datasets.zip',
        'url': 'https://drive.google.com/file/d/1i6hPUrY-VSJCMXXu7hgdBW2stAhVuCbj/view?usp=sharing'
    },
    3: {
        'id': '1jTl3D8SNI5D2AJ7RKxOvWCRRG_DYy1w1',
        'name': 'checkpoint.zip',
        'url': 'https://drive.google.com/file/d/1jTl3D8SNI5D2AJ7RKxOvWCRRG_DYy1w1/view?usp=sharing'
    }
}

class Downloader():

    def __init__(self, file_id, destination):
        self.URL = "https://docs.google.com/uc?export=download"
        self.file_id = file_id
        self.destination = destination

    def download_file_from_google_drive(self):
        session = requests.Session()
        response = session.get(self.URL, params = { 'id' : self.file_id }, stream = True)
        token = self.get_confirm_token(response)
        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(self.URL, params = params, stream = True)
        self.save_response_content(response, self.destination) 

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 1073741824
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    
    def unzipper(self, source_path, output_path):
        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)

if __name__ == '__main__':
    print('Preparing to download all necesary files...')

    if not os.path.exists('.temp/'):
        os.makedirs('.temp/')

    for key in files_to_download:
        name = files_to_download[key]['name']
        file_id = files_to_download[key]['id']
        destination = '.temp/' + name
        print(f'Downloading {name}...')
        downloader = Downloader(file_id=file_id, destination=destination)
        downloader.download_file_from_google_drive()
        #downloader.unzipper(source_path=destination, output_path=OUTPUT_PATH)

    #shutil.rmtree('.temp/')
NCP_Links = [f'http://ncov-ai.big.ac.cn/download/COVID19-{x}.zip' for x in range(1, 32)]
CP_Links = [f'http://ncov-ai.big.ac.cn/download/CP-{x}.zip' for x in range(1, 33)]
Normal_Links = [f'http://ncov-ai.big.ac.cn/download/Normal-{x}.zip' for x in range(1, 28)]

import os
import urllib
import urllib.request
import zipfile
import io

def download(url):
    with urllib.request.urlopen(url) as file:
        try:
            blocksize=100000
            file_path = os.getcwd() + '/' + file.info().get_filename()
            print(f"Downloading {file.info().get_filename()}")
            length = file.getheader('content-length')
            if length:
                length = int(length)
                blocksize = max(4096, length//100)
            print(length, blocksize)
            BufferAll = io.BytesIO()
            size = 0
            while True:
                BufferNow = file.read(blocksize)
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                size += len(BufferNow)
                if length:
                    percent = int((size / length)*100)
                    print(f"download: {percent}% {url}")

            print("Buffer All len:", len(BufferAll.getvalue()))

            with open(file_path, 'wb') as out_file:
                out_file.write(BufferAll.getbuffer())
                return file_path
        except urllib.error.HTTPError as e:
            print(e.__dict__)
            

def download_and_extract_to_folder(links, folder):
    if not os.path.isdir(folder):
        try:
            os.mkdir(folder)
        except OSError:
            print(f"Failed to create {folder}")
            return
        else:
            print(f"Created {folder}")

    for link in links:
        new_file = download(link)
        with zipfile.ZipFile(new_file, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.remove(new_file)

download_and_extract_to_folder(NCP_Links, 'NCP')
download_and_extract_to_folder(CP_Links, 'CP')
download_and_extract_to_folder(Normal_Links, 'Normal')

# cd "D:/CTR Pulmões - Doenças Respiratórias/CovidNet CT"
# mkdir "Base Formatada"
# python prepare_data.py "D:/CTR Pulmões - Doenças Respiratórias/CovidNet CT/" -o "D:/CTR Pulmões - Doenças Respiratórias/CovidNet CT/Base Formatada"


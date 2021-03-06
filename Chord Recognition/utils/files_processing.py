import urllib.request # download files folder
import os
import tarfile
import shutil # move files and delete folders with files

standard_file_url = 'http://www.isophonics.net/files/annotations/The%20Beatles%20Annotations.tar.gz'
local_file_name = 'The Beatles Annotations'
def download_uncompress_data_to_local(result_folder, file_url=standard_file_url):
    ORIGINAL_FOLDER = 'The Beatles Annotations'
    os.mkdir(result_folder)
    urllib.request.urlretrieve(file_url, local_file_name)
    with tarfile.open(local_file_name, "r:gz") as f:
        f.extractall('Beatles Annotations')

def filter_lab_files(search_folder, result_folder):
    folders_list_path = f'{search_folder}/chordlab/The Beatles'
    cd_folders = os.listdir(folders_list_path)
    for cd_folder in cd_folders:
        cd_folder_path = f'{folders_list_path}/{cd_folder}'
        for file_ in os.listdir(cd_folder_path):
            if(file_.endswith('.lab')):
                file_path = f'{cd_folder_path}/{file_}'
                shutil.copy(file_path, result_folder)

def delete_download_file(file):
    os.remove(file)

def delete_download_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)

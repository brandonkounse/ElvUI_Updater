import os
import requests
import zipfile
import shutil
from packaging import version

def is_newer_version(local_version, remote_version):
    return version.parse(remote_version) > version.parse(local_version)

def get_local_version_from_toc(toc_file_path):
    try:
        with open(toc_file_path, 'r') as file:
            for line in file:
                if '## Version:' in line:
                    return line.split(':', 1)[1].strip()
    except FileNotFoundError:
        print(f"TOC file not found at {toc_file_path}")
        return None

def get_elvui_info():
    api_url = "https://api.tukui.org/v1/addon/elvui"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'version': data['version'],
            'download_url': data['url'],
            'last_update': data['last_update']
        }
    else:
        print("Failed to retrieve data from TukUI API")
        return None
    
def download_elvui_zip(url, version):
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_to_save_as = os.path.join(downloads_dir, f'elvui-{version}.zip')

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_to_save_as, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded ElvUI version {version} to {file_to_save_as}")
    else:
        print("Failed to download the file")

def unzip_and_replace(zip_path, extract_to, target_dir, folders):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"Contents of {extract_to}:")
    [print(os.path.join(extract_to, f)) for f in os.listdir(extract_to)]

    for folder in folders:
        source_folder = os.path.join(extract_to, folder)
        target_folder = os.path.join(target_dir, folder)

        if os.path.exists(source_folder):
            if os.path.exists(target_folder):
                shutil.rmtree(target_folder)
            shutil.move(source_folder, target_dir)
        else:
            print(f"Folder '{folder}' not found in the extracted files.")


def print_header(title):
    print(f"\n{'=' * 20}\n{title}\n{'=' * 20}")


def main():
    elvui_dir = r'C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns'
    toc_file_path = os.path.join(elvui_dir, 'ElvUI', 'ElvUI_Mainline.toc')

    local_version = get_local_version_from_toc(toc_file_path)
    elvui_info = get_elvui_info()

    if elvui_info:
        print_header("ElvUI Update Check")

        print(f"Remote ElvUI Version: {elvui_info['version']}")
        print(f"Local ElvUI Version: {local_version or 'Not found'}")
        print(f"Last Update: {elvui_info['last_update']}")

        if local_version is None or is_newer_version(local_version, elvui_info['version']):
            print("\nUpdate required.")
            print("Starting download...")

            download_elvui_zip(elvui_info['download_url'], elvui_info['version'])

            downloaded_zip = os.path.join(os.path.expanduser('~'), 'Downloads', f'elvui-{elvui_info["version"]}.zip')
            extract_to_temp = os.path.join(os.path.expanduser('~'), 'Downloads', 'elvui_extracted')
            os.makedirs(extract_to_temp, exist_ok=True)

            folders_to_move = ['ElvUI', 'ElvUI_Libraries', 'ElvUI_Options']
            unzip_and_replace(downloaded_zip, extract_to_temp, elvui_dir, folders_to_move)

            shutil.rmtree(extract_to_temp)

            print("\nElvUI updated successfully.")
        else:
            print("\nNo update required.")

if __name__ == "__main__":
    main()

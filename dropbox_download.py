from dropbox_CRUD_2 import *
import os


def main():
    FILE_LIST = ['README.md', '2025-08-14 095025.254973README.md', '20250814_095346_README.md', '20250814_102144_README.md']

    REMOTE_WORK_FOLDER = '/data/test_folder'
    LOCAL_DESTINATION_FOLDER = r'd:/'

    for FILE_NAME in FILE_LIST:
        REMOTE_FILE_PATH = f'{REMOTE_WORK_FOLDER}/{FILE_NAME}'
        LOCAL_DESTINATION_PATH = os.path.join(LOCAL_DESTINATION_FOLDER, FILE_NAME)
        download_file(
            remote_file_path=REMOTE_FILE_PATH,
            local_destination_path=LOCAL_DESTINATION_PATH,
        )


if __name__ == "__main__":
    main()

# В директории `/data/test_folder` содержится:
# - 0 папок: []
# - 4 файла(ов) ['README.md', '2025-08-14 095025.254973README.md', '20250814_095346_README.md', '20250814_102144_README.md']

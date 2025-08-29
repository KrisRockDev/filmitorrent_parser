from dropbox_CRUD_2 import *


def main():
    LOCAL_ORIGINAL_FILE = 'README.md'
    REMOTE_WORK_FOLDER = '/data/test_folder'

    upload_file(
        local_file_path=LOCAL_ORIGINAL_FILE,
        remote_folder_path=REMOTE_WORK_FOLDER,
        now=True,
    )


if __name__ == "__main__":
    main()

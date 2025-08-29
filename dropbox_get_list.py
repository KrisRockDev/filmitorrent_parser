from dropbox_CRUD_2 import *


def main():
    REMOTE_WORK_FOLDER = '/data/test_folder'

    folders_list, files_list = list_folder(
        remote_folder_path=REMOTE_WORK_FOLDER,
    )

    print(f"В директории `{REMOTE_WORK_FOLDER}` содержится:\n- {len(folders_list)} папок: {folders_list}\n- {len(files_list)} файла(ов) {files_list}")

if __name__ == "__main__":
    main()


# В директории `/data/test_folder` содержится:
# - 0 папок: []
# - 4 файла(ов) ['README.md', '2025-08-14 095025.254973README.md', '20250814_095346_README.md', '20250814_102144_README.md']
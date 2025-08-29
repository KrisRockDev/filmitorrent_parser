import os
import datetime
from settings import LOGS_DIR_ABSOLUTE

def print_error(message):
    os.makedirs(LOGS_DIR_ABSOLUTE, exist_ok=True)
    file_name = str(datetime.datetime.now()).replace(':', '-')

    with open(file=os.path.join(LOGS_DIR_ABSOLUTE, file_name + '.log'), mode='a', encoding='utf-8') as f:
        f.write(f'{str(datetime.datetime.now())}\t{message}\n')
# UTILS


import logging
import os

from fastapi import FastAPI


log_format = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
logging.basicConfig(filename="error.log", level=logging.ERROR, format=log_format)

app = FastAPI()

separation_message_type = ": "


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


# Convert to human-readable format
def convert_bytes_to_mb(byte_size):
    megabyte_size = byte_size / (1024.0 * 1024.0)
    return megabyte_size
    # return f"{megabyte_size:.2f} MB"


def parse_error_message(exc):
    index = exc.detail.find(separation_message_type)

    if index != -1:
        error_type = exc.detail[:index]
        error_value = exc.detail[index + 2 :]

        error_object = {
            "type": f"{error_type} ({exc.status_code})",
            "message": error_value,
        }
        return error_object
    else:
        error_object = {"type": exc.status_code, "message": exc.detail}
        return error_object

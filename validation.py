# VALIDATION


import os

import magic
from exception import raise_exception

from utils import convert_bytes_to_mb, get_folder_size


invalid_name_characters = set(':*<>?/"')

sensitive_content = {"xxx", "sex", "porn"}

allowed_extensions = {"jpg", "jpeg", "png"}


async def check_file_name(file_name):
    if any(char in invalid_name_characters for char in file_name):
        error_code = 400
        raise raise_exception(
            error_code,
            "FilenameInvalid",
            f"File name: {file_name} is invalide, it contains one of these characters {invalid_name_characters}",
        )


async def check_sensitive_content(file_name):
    if any(content in file_name.lower() for content in sensitive_content):
        error_code = 400
        raise raise_exception(
            error_code,
            "SensitiveFileException",
            f"The file {file_name} contains sensitive content",
        )


async def check_duplication(file, folder_name: str):
    file_name = file.filename

    # Check if the folder exists
    if not os.path.exists(folder_name):
        raise FileNotFoundError(f"Folder '{folder_name}' not found.")

    # Check if the file exists in the folder
    file_path = os.path.join(folder_name, file_name)
    if os.path.isfile(file_path):
        error_code = 400
        raise raise_exception(
            error_code,
            "DuplicatedFile",
            f"file with name {file_name} already exists, rename the file to upload",
        )


# Check file storage size
async def check_storage_space_available(folder_path, max_storage_size, file):
    folder_size_bytes = get_folder_size(folder_path)
    folder_size_readable = convert_bytes_to_mb(folder_size_bytes)
    print(f"Total size of files in '{folder_path}': {folder_size_readable}")

    file_size = file.size / (1024.0 * 1024.0)

    required_size = file_size + folder_size_readable

    diff = max_storage_size - required_size

    if diff < 0:
        error_code = 507
        raise raise_exception(
            error_code,
            "InsufficientCloudStorage",
            f"{max_storage_size:.2f} MB maximum storage reached, need {-diff:.2f} MB more",
        )


# Check file size
async def check_file_size(file_size, max_size_mb=2):
    # Check if file size exceeds the allowed limit
    if file_size > max_size_mb * 1024 * 1024:
        error_code = 413
        raise raise_exception(
            error_code,
            "FileTooLarge",
            f"File size exceeds the allowed limit ({max_size_mb} MB)",
        )


# Check file type
async def check_image_type(file):
    file_bytes = await file.read()
    type_description = magic.from_buffer(file_bytes)
    print(type_description)
    file_extension = file.filename.split(".")[-1].lower()
    if "image" not in type_description and file_extension in allowed_extensions:
        raise raise_exception(
            500, "CorruptedFile", f"{file.filename} is a corrupted image file"
        )
    if "image" in type_description and file_extension not in allowed_extensions:
        raise raise_exception(
            401,
            "NotAuthorized",
            f"Image with extension {file_extension} is not authorized",
        )
    if "image" not in type_description and file_extension not in allowed_extensions:
        raise raise_exception(
            400,
            "BadFileType",
            f"{file.filename} don't have correct file type {allowed_extensions}",
        )


# Check if the file is empty
async def check_file_content(files):
    for file in files:
        if not file:
            error_code = 400
            raise raise_exception(
                error_code,
                "BadRequest",
                "No file attached to the request)",
            )

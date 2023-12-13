import schedule
import time
import magic
from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import logging
import threading
import os
import traceback

log_format = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
logging.basicConfig(filename="error.log", level=logging.ERROR, format=log_format)

app = FastAPI()

separation_message_type = ": "

PICTURE_FOLDER = "Pictures"

invalid_name_characters = set(':*<>?/"')

sensitive_content = {"Xxx", "Sex", "porn"}

allowed_extensions = {"jpg", "jpeg", "png"}

not_legal_image_name = ["not_legal.jpg", "forbidden_document.jpg", "pirate.jpg"]

request_count = 0

error_status_codes = [400, 402, 403, 501]

not_legal_image_name = ["not_legal.jpg", "forbidden_document.jpg", "pirate.jpg"]

looked_image_name = ["sensitive_business_file.jpg", "personal_file.jpg"]


def reset_request_count():
    global request_count
    request_count = 0


# UTILS


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


# VALIDATION


async def check_file_name(file_name):
    if any(char in invalid_name_characters for char in file_name):
        error_code = 400
        raise raise_exception(
            error_code,
            "FilenameInvalid",
            f"File name: {file_name} is invalide, it contains one of these characters {invalid_name_characters}",
        )


async def check_sensitive_content(file_name):
    if any(content in sensitive_content for content in file_name):
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


# CUSTOM EXCEPTIONS


@app.middleware("http")
async def set_timeout(request: Request, call_next):
    response = await call_next(request)
    response.timeout = 5  # seconds
    return response


def cast_message_to_exception_message(error_type, message):
    return f"{error_type}{separation_message_type}{message}"


schedule.every(2).seconds.do(reset_request_count)


# thread = threading.Timer(1, lambda: globals().update(raise_exception(408, "RequestTimeout", f"message")))


def raise_exception(code, type, message):
    msg_error = cast_message_to_exception_message(type, message)
    return HTTPException(status_code=code, detail=msg_error)


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


@app.get("/ping")
def disp_error():
    return "pong"


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_trace = traceback.format_exc()
    logging.error(error_trace)
    logging.error(" --- --- --- --- --- --- --- --- ---" + "\n" + "\n")
    error_message = parse_error_message(exc)
    return JSONResponse(status_code=exc.status_code, content=error_message)


for status_code in error_status_codes:

    @app.exception_handler(status_code)
    async def specific_exception_handler(request, exc):
        error_message = parse_error_message(exc)
        return JSONResponse(status_code=exc.status_code, content=error_message)


@app.delete("/picture")
def delete_file():
    try:
        raise raise_exception(
            501, "NotImplemented", f"the endpoint /delete is not implemented "
        )
    except HTTPException as e:
        logging.error(e.detail)
        raise e

@app.get("/divs-by-0")
def divs_by_0():
    try:
        x = 1 / 0
    except Exception as e:
        logging.error(e)
        raise raise_exception(
            500,
            "ServerErrorException",
            f"an error has occurred in the server / {e}"
        )


@app.get("/in-maintenance")
def in_maintenance():
    try:
        raise raise_exception(
            503, "ServiceUnavailable", f"the service u want to use in in  maintenance."
        )
    except HTTPException as e:
        logging.error(e.detail)
        raise e


# Endpoint that checks the value of the query parameter "n"
@app.get("/picture")
async def get_picture(
    file_name: str = Query(..., description="Name of the image file"),
):
    try:
        schedule.run_pending()
        global request_count
        request_count += 1
        file_path = os.path.join(PICTURE_FOLDER, file_name)
        print(file_path)
        if request_count > 2:
            raise raise_exception(
                429,
                "TooManyRequest",
                f"must not execute request more than 2 times per second",
            )
        if file_name in not_legal_image_name:
            raise raise_exception(
                453,
                "LegalReason",
                f"the file with name '{file_name}' cannot be downloaded for legal reasons",
            )

        if file_name in looked_image_name:
            raise raise_exception(
                423,
                "LockedException",
                f"the file with name '{file_name}' is looked, so it cannot be downloaded",
            )

        if not os.path.exists(file_path):
            raise raise_exception(
                404, "FileNotFound", f"the file with name '{file_name}' is not found."
            )

        media_type="image/jpeg"
        if('.png' in file_name):
            media_type = "image/png"
        elif('.webp' in file_name):
            media_type = "image/webp"

        return FileResponse(
            file_path,
            media_type=media_type,
            headers={"Content-Disposition": f"filename={file_name}"},
        )
    except TimeoutError as e:
        logging.error(e.detail)
        raise raise_exception(408, "RequestTimeout", f"message")
    except Exception as e:
        logging.error(e.detail)
        raise e


@app.post("/pictures")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        schedule.run_pending()
        global request_count
        request_count += 1

        await check_file_content(files)
        uploaded_files = []
        print(files)
        print(files.count)
        for file in files:
            await check_file_size(file.size)
            await check_duplication(file, PICTURE_FOLDER)
            await check_file_name(file.filename)
            await check_image_type(file)
            await check_sensitive_content(file.filename)
            max_storage_size_mb = 6
            await check_storage_space_available(
                PICTURE_FOLDER, max_storage_size_mb, file
            )

            # Save the file to the 'images' folder
            with open(f"{PICTURE_FOLDER}/{file.filename}", "wb") as image_file:
                image_file.write(file.file.read())

            uploaded_files.append(
                {"filename": file.filename, "content_type": file.content_type}
            )

        if request_count > 2:
            raise raise_exception(
                429,
                "TooManyRequest",
                f"must not execute request more than 2 times per second",
            )

        if 20000 < 100:
            raise raise_exception(
                507, "StockageInsufisantCloud", f"{n} must be greater than 100"
            )
        if 20000 < 100:
            raise raise_exception(413, "FileTooLarge", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(401, "NotAuthorize", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(400, "SensitiveFile", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(
                400, "FileNameInvafilelid", f"{n} must be greater than 100"
            )
        if 20000 < 100:
            raise raise_exception(400, "BadFileType", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(
                429, "TooManyRequest", f"{n} must be greater than 100"
            )
        if 20000 < 100:
            raise raise_exception(
                408, "RequestTimeout", f"{n} must be greater than 100"
            )
        if 20000 < 100:
            raise raise_exception(
                501, "NotImplemented", f"{n} must be greater than 100"
            )
        if 20000 < 100:
            raise raise_exception(400, "DuplicateFile", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(500, "CorruptedFile", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(423, "LockException", f"{n} must be greater than 100")

        return {"uploaded_files": uploaded_files}

    except Exception as e:
        logging.error(e.detail)
        raise e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

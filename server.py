import schedule
import time
import magic
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import logging
import threading
import os


log_format = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
logging.basicConfig(filename="error.log", level=logging.ERROR, format=log_format)

app = FastAPI()

separation_message_type = ": "

request_count = 0

error_status_codes = [400, 402, 403, 501]

not_legal_image_name = ["not_legal.jpg", "forbidden_document.jpg", "pirate.jpg"]


def reset_request_count():
    global request_count
    request_count = 0


allowed_extensions = {"jpg", "jpeg", "png", "webp"}


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


# Check file size
async def check_file_extension(file):
    # Check if the file extension is allowed
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise raise_exception(
            400,
            "BadFileType",
            f"{file.filename} don't have a valid extension (jpg, jpeg, png)",
        )


async def check_corrupted_image(file):
    file_bytes = await file.read()
    type_description = magic.from_buffer(file_bytes)
    print(type_description)
    file_extension = file.filename.split(".")[-1].lower()
    if "image" not in type_description and file_extension in allowed_extensions:
        raise raise_exception(
            500, "CorruptedFile", f"{file.filename} is a corrupted image file"
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


# V
def cast_message_to_exception_message(error_type, message):
    return f"{error_type}{separation_message_type}{message}"


schedule.every(2).seconds.do(reset_request_count)


# thread = threading.Timer(1, lambda: globals().update(raise_exception(408, "RequestTimeout", f"message")))


def raise_exception(code, tyme, message):
    msg_error = cast_message_to_exception_message(tyme, message)
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
    error_message = parse_error_message(exc)
    return JSONResponse(status_code=exc.status_code, content=error_message)


for status_code in error_status_codes:

    @app.exception_handler(status_code)
    async def specific_exception_handler(request, exc):
        error_message = parse_error_message(exc)
        return JSONResponse(status_code=exc.status_code, content=error_message)


@app.get("/pictures")
def delete_file():
    try:
        raise raise_exception(
            501, "NotImplemented", f"the endpoint /delete is not implemented "
        )
    except HTTPException as e:
        logging.error(e.detail)
        raise e


@app.get("/in-maintenance")
def delete_file():
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
        # thread.start()
        schedule.run_pending()
        global request_count
        request_count += 1
        file_path = os.path.join("Pictures", file_name)

        if request_count > 2:
            raise raise_exception(
                429,
                "TooManyRequest",
                f"must not execute request more than 2 times per second",
            )

        if not os.path.exists(file_path):
            raise raise_exception(
                404, "FileNotFound", f"the file with name '{file_name}' is not found."
            )

        if file_name in not_legal_image_name:
            raise raise_exception(
                453,
                "LegalReason",
                f"the file with name '{file_name}' cannot be downloaded for legal reasons",
            )
        return FileResponse(
            file_path,
            media_type="image/jpeg",
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
        await check_file_content(files)

        uploaded_files = []
        print(files)
        print(files.count)
        for file in files:
            await check_file_size(file.size)
            await check_file_extension(file)
            await check_corrupted_image(file)

            # Save the file to the 'images' folder
            with open(f"Pictures/{file.filename}", "wb") as image_file:
                image_file.write(file.file.read())

            uploaded_files.append(
                {"filename": file.filename, "content_type": file.content_type}
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
                400, "FileNameInvalid", f"{n} must be greater than 100"
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
        # logging.error(e.detail)
        raise e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

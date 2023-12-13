import asyncio
import time
from datetime import datetime
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import logging
import os

log_format = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
logging.basicConfig(filename="error.log", level=logging.ERROR, format=log_format)

app = FastAPI()

separation_message_type = ": "

error_status_codes = [400, 402, 403]


def cast_message_to_exception_message(error_type, message):
    return f"{error_type}{separation_message_type}{message}"


def raise_exception(code, tyme, message):
    msg_error = cast_message_to_exception_message(tyme, message)
    return HTTPException(status_code=code, detail=msg_error)


def parse_error_message(exc):
    index = exc.detail.find(separation_message_type)

    if index != -1:
        error_type = exc.detail[:index]
        error_value = exc.detail[index + 2:]

        error_object = {"type": f"{error_type} ({exc.status_code})", "message": error_value}
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
    return JSONResponse(
        status_code=exc.status_code,
        content=error_message
    )


for status_code in error_status_codes:
    @app.exception_handler(status_code)
    async def specific_exception_handler(request, exc):
        error_message = parse_error_message(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_message
        )


# Endpoint that checks the value of the query parameter "n"
@app.get("/picture")
async def get_picture(
        file_name: str = Query(..., description="Name of the image file"),
):
    try:
        file_path = os.path.join("picture", file_name)
        if not os.path.exists(file_path):
            raise raise_exception(404, "FileNotFound", f"{file_name} is not found.")

        time.sleep(60)

        if 1 == 2:
            raise raise_exception(501, "NotImplemented", f"message")
        if 1 == 2:
            raise raise_exception(453, "LegalReason", f"message")
        if 1 == 2:
            raise raise_exception(429, "TooManyRequest", f"message")

        return FileResponse(file_path, media_type="image/jpeg",
                            headers={"Content-Disposition": f"filename={file_name}"})
    except TimeoutError as e:
        logging.error(exc.detail)
        raise raise_exception(408, "RequestTimeout", f"message")
    except Exception as e:
        logging.error(e.detail)
        raise e


@app.post("/pictures")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        uploaded_files = []

        for file in files:
            # Check if the file extension is allowed
            allowed_extensions = {"jpg", "jpeg", "png"}
            file_extension = file.filename.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise raise_exception(400, "DuplicateFile", f"{file.filename} already exist.")

            # Check the real file format (mime type)
            allowed_mime_types = {"image/jpeg", "image/png"}
            if file.content_type not in allowed_mime_types:
                raise raise_exception(400, "BadFileType", f"{file.filename} must be .jpg, .jpeg or .png")

            # Save the file to the 'images' folder
            with open(f"picture/{file.filename}", "wb") as image_file:
                image_file.write(file.file.read())

            uploaded_files.append(
                {"filename": file.filename, "content_type": file.content_type}
            )

        if 20000 < 100:
            raise raise_exception(507, "StockageInsufisantCloud", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(413, "FileTooLarge", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(401, "NotAuthorize", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(400, "SensitiveFile", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(400, "FileNameInvalid", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(400, "BadFileType", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(429, "TooManyRequest", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(408, "RequestTimeout", f"{n} must be greater than 100")
        if 20000 < 100:
            raise raise_exception(501, "NotImplemented", f"{n} must be greater than 100")
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

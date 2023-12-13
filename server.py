import schedule
from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import logging
import os
import traceback
from exception import raise_exception
from utils import app

from validation import (
    check_duplication,
    check_file_content,
    check_file_name,
    check_file_size,
    check_image_type,
    check_sensitive_content,
    check_storage_space_available,
)


PICTURE_FOLDER = "Pictures"

not_legal_image_name = ["not_legal.jpg", "forbidden_document.jpg", "pirate.jpg"]

request_count = 0

looked_image_name = ["sensitive_business_file.jpg", "personal_file.jpg"]


def reset_request_count():
    global request_count
    request_count = 0


schedule.every(2).seconds.do(reset_request_count)


# thread = threading.Timer(1, lambda: globals().update(raise_exception(408, "RequestTimeout", f"message")))


@app.get("/ping")
def disp_error():
    return "pong"


@app.delete("/picture")
def delete_file():
    try:
        raise raise_exception(
            501, "NotImplemented", "the endpoint /delete is not implemented "
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
            500, "ServerErrorException", f"an error has occurred in the server / {e}"
        )


@app.get("/in-maintenance")
def in_maintenance():
    try:
        raise raise_exception(
            503, "ServiceUnavailable", "the service u want to use in in  maintenance."
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

        media_type = "image/jpeg"
        if ".png" in file_name:
            media_type = "image/png"
        elif ".webp" in file_name:
            media_type = "image/webp"

        return FileResponse(
            file_path,
            media_type=media_type,
            headers={"Content-Disposition": f"filename={file_name}"},
        )
    except TimeoutError as e:
        logging.error(e.detail)
        raise raise_exception(408, "RequestTimeout", "Timeout")
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
                "must not execute request more than 2 times per second",
            )

        return {"uploaded_files": uploaded_files}

    except Exception as e:
        logging.error(e.detail)
        raise e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

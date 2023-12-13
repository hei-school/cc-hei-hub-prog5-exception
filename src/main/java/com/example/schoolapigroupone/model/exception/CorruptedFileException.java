package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class CorruptedFileException extends ApiException {

    private final HttpStatus httpStatus;

    public CorruptedFileException() {
        super(ExceptionType.CLIENT_EXCEPTION, "Corrupted file.");
        this.httpStatus = HttpStatus.BAD_REQUEST;
    }

    public CorruptedFileException(String message, HttpStatus httpStatus) {
        super(ExceptionType.CLIENT_EXCEPTION, message);
        this.httpStatus = httpStatus;
    }

    public HttpStatus getHttpStatus() {
        return httpStatus;
    }
}

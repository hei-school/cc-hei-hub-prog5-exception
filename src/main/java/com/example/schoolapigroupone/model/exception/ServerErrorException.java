package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class ServerErrorException extends ApiException{

    private final HttpStatus httpStatus;

    public ServerErrorException() {
        super(ExceptionType.SERVER_EXCEPTION, "Server error.");
        this.httpStatus = HttpStatus.INTERNAL_SERVER_ERROR;
    }

    public ServerErrorException(String message, HttpStatus httpStatus) {
        super(ExceptionType.SERVER_EXCEPTION, message);
        this.httpStatus = httpStatus;
    }

    public HttpStatus getHttpStatus() {
        return httpStatus;
    }
}

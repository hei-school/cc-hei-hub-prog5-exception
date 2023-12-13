package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class TooManyRequestException extends ApiException {
    private final HttpStatus httpStatus;

    public TooManyRequestException() {
        super(ExceptionType.CLIENT_EXCEPTION, "Too many requests");
        this.httpStatus = HttpStatus.TOO_MANY_REQUESTS;
    }

    public TooManyRequestException(String message, HttpStatus httpStatus) {
        super(ExceptionType.CLIENT_EXCEPTION, message);
        this.httpStatus = httpStatus;
    }

    public HttpStatus getHttpStatus() {
        return httpStatus;
    }
}
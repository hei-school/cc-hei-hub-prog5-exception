package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class ForLegalReasonException extends ApiException{
    private final HttpStatus httpStatus;

    public ForLegalReasonException() {
        super(ExceptionType.SERVER_EXCEPTION, "Service unavailable for legal reasons.");
        this.httpStatus = HttpStatus.BAD_REQUEST;
    }

    public ForLegalReasonException(String message, HttpStatus httpStatus) {
        super(ExceptionType.SERVER_EXCEPTION, message);
        this.httpStatus = httpStatus;
    }

    public HttpStatus getHttpStatus() {
        return httpStatus;
    }
}

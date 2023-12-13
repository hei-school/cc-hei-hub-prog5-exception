package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class NotImplementedException extends ApiException{
    private final HttpStatus httpStatus;

    public NotImplementedException() {
        super(ExceptionType.SERVER_EXCEPTION, "Function not implemented.");
        this.httpStatus = HttpStatus.NOT_IMPLEMENTED;
    }

    public NotImplementedException(String message, HttpStatus httpStatus) {
        super(ExceptionType.SERVER_EXCEPTION, message);
        this.httpStatus = httpStatus;
    }
    public HttpStatus getHttpStatus() {
        return httpStatus;
    }
}

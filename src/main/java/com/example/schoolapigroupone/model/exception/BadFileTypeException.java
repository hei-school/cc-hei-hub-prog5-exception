package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class BadFileTypeException extends ApiException {

  private final HttpStatus httpStatus;

  public BadFileTypeException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Invalid or unsupported file type");
    this.httpStatus = HttpStatus.BAD_REQUEST;
  }

  public BadFileTypeException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

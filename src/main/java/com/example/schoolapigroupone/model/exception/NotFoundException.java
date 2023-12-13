package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class NotFoundException extends ApiException {

  private final HttpStatus httpStatus;

  public NotFoundException() {
    super(ExceptionType.SERVER_EXCEPTION, "File not found");
    this.httpStatus = HttpStatus.NOT_FOUND;
  }

  public NotFoundException(String message, HttpStatus httpStatus) {
    super(ExceptionType.SERVER_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

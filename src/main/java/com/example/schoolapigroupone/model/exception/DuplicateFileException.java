package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class DuplicateFileException extends ApiException {

  private final HttpStatus httpStatus;

  public DuplicateFileException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Duplicated file");
    this.httpStatus = HttpStatus.BAD_REQUEST;
  }

  public DuplicateFileException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

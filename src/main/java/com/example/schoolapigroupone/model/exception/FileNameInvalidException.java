package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class FileNameInvalidException extends ApiException {

  private final HttpStatus httpStatus;

  public FileNameInvalidException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Invalid file name");
    this.httpStatus = HttpStatus.BAD_REQUEST;
  }

  public FileNameInvalidException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

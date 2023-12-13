package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class SensitiveFileException extends ApiException {

  private final HttpStatus httpStatus;

  public SensitiveFileException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Access is denied due to sensitive information");
    this.httpStatus = HttpStatus.BAD_REQUEST;
  }

  public SensitiveFileException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

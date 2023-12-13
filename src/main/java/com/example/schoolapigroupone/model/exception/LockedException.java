package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class LockedException extends ApiException {

  private final HttpStatus httpStatus;

  public LockedException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Locked file.");
    this.httpStatus = HttpStatus.LOCKED;
  }

  public LockedException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

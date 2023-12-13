package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class NotAuthorizedException extends ApiException {

  private final HttpStatus httpStatus;

  public NotAuthorizedException() {
    super(ExceptionType.CLIENT_EXCEPTION, "Not authorized to post in the wrong directory");
    this.httpStatus = HttpStatus.UNAUTHORIZED;
  }

  public NotAuthorizedException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

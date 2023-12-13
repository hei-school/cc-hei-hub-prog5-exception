package com.example.schoolapigroupone.model.exception;

import org.springframework.http.HttpStatus;

public class LargeFileException extends ApiException {

  private final HttpStatus httpStatus;

  public LargeFileException() {
    super(ExceptionType.CLIENT_EXCEPTION, "File too large");
    this.httpStatus = HttpStatus.PAYLOAD_TOO_LARGE;
  }

  public LargeFileException(String message, HttpStatus httpStatus) {
    super(ExceptionType.CLIENT_EXCEPTION, message);
    this.httpStatus = httpStatus;
  }

  public HttpStatus getHttpStatus() {
    return httpStatus;
  }
}

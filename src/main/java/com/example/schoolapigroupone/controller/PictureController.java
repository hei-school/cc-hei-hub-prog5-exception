package com.example.schoolapigroupone.controller;

import com.example.schoolapigroupone.model.Picture;
import com.example.schoolapigroupone.model.exception.*;
import com.example.schoolapigroupone.service.PictureService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

@RestController
@AllArgsConstructor
public class PictureController {
  private final PictureService pictureService;

  private static final Logger logger = LoggerFactory.getLogger(PictureController.class);

  @GetMapping("/ping")
  public String ping() {
    return "pong";
  }

  @PostMapping("/picture")
  public ResponseEntity<String> uploadPicture(@RequestBody Picture picture) {
    try {
      return pictureService.uploadPicture(picture);
    } catch (TooManyRequestException e) {
      return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
              .body(e.getHttpStatus() + ": " + e.getMessage());
    } catch (SensitiveFileException e) {
      logger.error("SensitiveFileException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.BAD_REQUEST);
    } catch (NotAuthorizedException e) {
      logger.error("NotAuthorizedException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.FORBIDDEN);
    } catch (BadFileTypeException e) {
      logger.error("BadFileTypeException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.BAD_REQUEST);
    } catch (FileNameInvalidException e) {
      logger.error("FileNameInvalidException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.BAD_REQUEST);
    } catch (DuplicateFileException e) {
      logger.error("DuplicateFileException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.BAD_REQUEST);
    } catch (LargeFileException e) {
      logger.error("LargeFileException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.REQUEST_HEADER_FIELDS_TOO_LARGE);
    } catch (CorruptedFileException e) {
      logger.error("CorruptedFileException during uploadPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.BAD_REQUEST);
    } catch (Exception e) {
      logger.error("Exception during uploadPicture", e);
      return new ResponseEntity<>("Unexpected error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  @GetMapping("/picture/{label}")
  public ResponseEntity<?> getPictureByLabel(@PathVariable String label) throws Exception {
    Picture picture = pictureService.getPictureByLabel(label);
      try {
        return ResponseEntity.ok(picture);
      } catch (TooManyRequestException e) {
        logger.error("TooManyRequestException during gettingPicture", e);
        return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
                .body(e.getHttpStatus() + ": " + e.getMessage());
      }catch (ForLegalReasonException e) {
        logger.error("ForLegalReasonException during gettingPicture", e);
        return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.UNAVAILABLE_FOR_LEGAL_REASONS);
      } catch (NotFoundException e) {
        logger.error("NotFoundException during gettingPicture", e);
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(e.getHttpStatus() + ": " + e.getMessage());
      } catch (Exception e) {
        logger.error("Exception during gettingPicture", e);
        return new ResponseEntity<>("Unexpected error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
      }

  }

  @GetMapping("/pictures")
  public ResponseEntity<?> getPictures() {
    try {
      throw new NotImplementedException();
    } catch (TooManyRequestException e) {
      logger.error("TooManyRequestException during gettingPictures", e);
      return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
              .body(e.getHttpStatus() + ": " + e.getMessage());
    }catch (NotImplementedException e) {
      logger.error("NotImplementedException during gettingPictures", e);
      return ResponseEntity.status(HttpStatus.NOT_IMPLEMENTED)
              .body(HttpStatus.NOT_IMPLEMENTED + ": " + e.getMessage());
    }
  }

  @GetMapping("/divs-by-0")
  public ResponseEntity<?> divsByZero(){
    try{
      int number = pictureService.getDirectoriesSize();
      return ResponseEntity.ok(number);
    } catch (TooManyRequestException e) {
      logger.error("TooManyRequestException during divs-by-0", e);
      return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
              .body(e.getHttpStatus() + ": " + e.getMessage());
    } catch (ServerErrorException e){
      logger.error("ServerErrorException during divs-by-0", e);
      return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
              .body(e.getHttpStatus() + ": " + e.getMessage());
    }
  }

  @DeleteMapping("/pictures/{id}")
  public ResponseEntity<?> deletePictureById (@PathVariable Long id){
    try {
      pictureService.deletePictureById(id);
      return ResponseEntity.ok("Picture with ID " + id + " has been deleted.");
    } catch (ServiceUnavailableException e) {
      logger.error("ServiceUnavailableException during delettingPicture", e);
      return new ResponseEntity<>(e.getHttpStatus() + ": " + e.getMessage(), HttpStatus.SERVICE_UNAVAILABLE);
    }
  }

@GetMapping("/simulate-timeout")
  public ResponseEntity<String> simulateTimeout() {
    try {
      CompletableFuture<ResponseEntity<String>> result = CompletableFuture.supplyAsync(() -> {
        try {
          Thread.sleep(30000);
          return ResponseEntity.ok("Request completed successfully after delay.");
        } catch (InterruptedException e) {
          logger.error("InterruptedException during simulating timeout", e);
          Thread.currentThread().interrupt();
          return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                  .body("Error occurred during simulation");
        }
      });

      return result.get(6, TimeUnit.SECONDS); // Timeout set to 6 seconds
    } catch (InterruptedException | ExecutionException | TimeoutException e) {
      logger.error("InterruptedException during simulating timeout after 6 seconds", e);
      return ResponseEntity.status(HttpStatus.REQUEST_TIMEOUT).body("Request timed out with status code " + HttpStatus.REQUEST_TIMEOUT.value());
    }
  }
}

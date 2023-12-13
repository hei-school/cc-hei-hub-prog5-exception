package com.example.schoolapigroupone.service;
import com.example.schoolapigroupone.model.Picture;
import com.example.schoolapigroupone.model.exception.*;
import com.example.schoolapigroupone.model.interceptor.RateLimitInterceptor;
import com.example.schoolapigroupone.model.exception.ServiceUnavailableException;
import com.example.schoolapigroupone.repository.PictureRepository;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Optional;

@Service
@AllArgsConstructor
@Getter
@Setter
public class PictureService {

  private final PictureRepository pictureRepository;
  private final ValidationService validationService;

@Autowired
  private RateLimitInterceptor rateLimitInterceptor;

  @Autowired
  private HttpServletRequest request;

  @Autowired
  private HttpServletResponse response;

  public ResponseEntity<String> uploadPicture(Picture picture) throws Exception {
    rateLimitInterceptor.preHandle(request, response, null);
    if (!validationService.isValidLabel(picture.getLabel())) {
      throw new SensitiveFileException();
    } else if(!validationService.isCorruptedFile(picture.getExtension(), picture.getBase64())){
      throw new CorruptedFileException();
    }else if (!validationService.isValidDirectory(picture.getDirectory())) {
      throw new NotAuthorizedException();
    } else if (!validationService.isValidFileType(picture.getExtension())) {
      throw new BadFileTypeException();
    } else if (!validationService.isValidFileName(picture.getLabel())) {
      throw new FileNameInvalidException();
    }  else if (!validationService.isNotDuplicated(picture.getLabel())) {
      throw new DuplicateFileException();
    }  else if (!validationService.isLargeFile(picture.getBase64())) {
      throw new LargeFileException();
    }

    Picture savedPicture = savePicture(picture);

    if (savedPicture != null) {
      return new ResponseEntity<>("Picture uploaded successfully", HttpStatus.OK);
    } else {
      return new ResponseEntity<>("Failed to upload picture", HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  public Picture savePicture(Picture picture) throws Exception {
    rateLimitInterceptor.preHandle(request, response, null);
    return pictureRepository.save(picture);
  }

  public Picture getPictureByLabel(String label) throws Exception {
    rateLimitInterceptor.preHandle(request, response, null);
    Optional<Picture> picture = pictureRepository.findPictureByLabel(label);
    if(!picture.isPresent()){
      if (validationService.isAvailableForLegalReason(label)){
        throw new ForLegalReasonException();
      }else if(getValidationService().isLocked(label)){
        throw new LockedException();
      }else{
        throw new NotFoundException();
      }
    }else{
        return  picture.get();
    }
  }
  public void deletePictureById(Long id) {
    throw new ServiceUnavailableException();
  }

  public int getDirectoriesSize() {
    try{
      int number = 785689/0;
      return number;
    }catch (Exception e) {
      throw new ServerErrorException();
    }
  }

}

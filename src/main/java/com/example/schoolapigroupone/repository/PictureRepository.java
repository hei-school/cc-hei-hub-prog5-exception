package com.example.schoolapigroupone.repository;

import com.example.schoolapigroupone.model.Picture;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PictureRepository extends JpaRepository<Picture, Long> {
    Optional<Picture> findPictureByLabel(String label);
}
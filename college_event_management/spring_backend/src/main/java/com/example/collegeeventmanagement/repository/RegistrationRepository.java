package com.example.collegeeventmanagement.repository;

import com.example.collegeeventmanagement.model.Registration;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RegistrationRepository extends MongoRepository<Registration, String> {
    List<Registration> findByUserId(String userId);
    List<Registration> findByEventId(String eventId);
    List<Registration> findByStatus(String status);
}

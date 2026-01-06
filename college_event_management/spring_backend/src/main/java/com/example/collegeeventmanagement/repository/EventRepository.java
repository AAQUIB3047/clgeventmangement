package com.example.collegeeventmanagement.repository;

import com.example.collegeeventmanagement.model.Event;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface EventRepository extends MongoRepository<Event, String> {
    List<Event> findByStatus(String status);
    List<Event> findByCreatedAtAfter(LocalDateTime dateTime);
    List<Event> findTop5ByOrderByCreatedAtDesc();
}

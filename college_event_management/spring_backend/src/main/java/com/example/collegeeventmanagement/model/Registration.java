package com.example.collegeeventmanagement.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Document(collection = "registrations")
public class Registration {
    @Id
    private String id;
    @DBRef
    private User user;
    @DBRef
    private Event event;
    private String status; // pending, confirmed, cancelled
    private LocalDateTime registeredAt;

    // Constructors
    public Registration() {}

    public Registration(User user, Event event, String status) {
        this.user = user;
        this.event = event;
        this.status = status;
        this.registeredAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }

    public Event getEvent() { return event; }
    public void setEvent(Event event) { this.event = event; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public LocalDateTime getRegisteredAt() { return registeredAt; }
    public void setRegisteredAt(LocalDateTime registeredAt) { this.registeredAt = registeredAt; }
}

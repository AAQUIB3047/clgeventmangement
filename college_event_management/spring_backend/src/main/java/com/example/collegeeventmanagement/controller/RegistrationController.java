package com.example.collegeeventmanagement.controller;

import com.example.collegeeventmanagement.model.Registration;
import com.example.collegeeventmanagement.service.RegistrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/registrations")
@CrossOrigin(origins = "*")
public class RegistrationController {

    @Autowired
    private RegistrationService registrationService;

    @GetMapping
    public ResponseEntity<List<Registration>> getAllRegistrations() {
        List<Registration> registrations = registrationService.getAllRegistrations();
        return ResponseEntity.ok(registrations);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Registration> getRegistrationById(@PathVariable String id) {
        Optional<Registration> registration = registrationService.getRegistrationById(id);
        if (registration.isPresent()) {
            return ResponseEntity.ok(registration.get());
        }
        return ResponseEntity.notFound().build();
    }

    @PostMapping
    public ResponseEntity<Registration> createRegistration(@RequestBody Registration registration) {
        Registration createdRegistration = registrationService.createRegistration(registration);
        return ResponseEntity.ok(createdRegistration);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Registration> updateRegistration(@PathVariable String id, @RequestBody Registration registrationDetails) {
        Registration updatedRegistration = registrationService.updateRegistration(id, registrationDetails);
        if (updatedRegistration != null) {
            return ResponseEntity.ok(updatedRegistration);
        }
        return ResponseEntity.notFound().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteRegistration(@PathVariable String id) {
        registrationService.deleteRegistration(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/event/{eventId}")
    public ResponseEntity<List<Registration>> getRegistrationsByEvent(@PathVariable String eventId) {
        List<Registration> registrations = registrationService.getRegistrationsByEvent(eventId);
        return ResponseEntity.ok(registrations);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Registration>> getRegistrationsByUser(@PathVariable String userId) {
        List<Registration> registrations = registrationService.getRegistrationsByUser(userId);
        return ResponseEntity.ok(registrations);
    }
}

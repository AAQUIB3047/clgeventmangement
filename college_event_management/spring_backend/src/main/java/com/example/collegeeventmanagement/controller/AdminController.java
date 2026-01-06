package com.example.collegeeventmanagement.controller;

import com.example.collegeeventmanagement.model.Event;
import com.example.collegeeventmanagement.model.User;
import com.example.collegeeventmanagement.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminController {

    @Autowired
    private AdminService adminService;

    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboardData() {
        Map<String, Object> data = adminService.getDashboardData();
        return ResponseEntity.ok(data);
    }

    @GetMapping("/users")
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = adminService.getAllUsers();
        return ResponseEntity.ok(users);
    }

    @PostMapping("/users")
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User createdUser = adminService.createUser(user);
        return ResponseEntity.ok(createdUser);
    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable String id) {
        adminService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/events")
    public ResponseEntity<List<Event>> getAllEvents() {
        List<Event> events = adminService.getAllEvents();
        return ResponseEntity.ok(events);
    }

    @PostMapping("/events")
    public ResponseEntity<Event> createEvent(@RequestBody Event event) {
        Event createdEvent = adminService.createEvent(event);
        return ResponseEntity.ok(createdEvent);
    }

    @PatchMapping("/events/{id}")
    public ResponseEntity<Event> updateEvent(@PathVariable String id, @RequestBody Map<String, Object> updates) {
        Event eventUpdates = new Event();
        if (updates.containsKey("status")) {
            eventUpdates.setStatus((String) updates.get("status"));
        }
        // Add other fields as needed
        Event updatedEvent = adminService.updateEvent(id, eventUpdates);
        if (updatedEvent != null) {
            return ResponseEntity.ok(updatedEvent);
        }
        return ResponseEntity.notFound().build();
    }

    @DeleteMapping("/events/{id}")
    public ResponseEntity<Void> deleteEvent(@PathVariable String id) {
        adminService.deleteEvent(id);
        return ResponseEntity.noContent().build();
    }
}

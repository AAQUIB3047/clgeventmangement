package com.example.collegeeventmanagement.service;

import com.example.collegeeventmanagement.model.Event;
import com.example.collegeeventmanagement.model.User;
import com.example.collegeeventmanagement.repository.EventRepository;
import com.example.collegeeventmanagement.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class AdminService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EventRepository eventRepository;

    public Map<String, Object> getDashboardData() {
        Map<String, Object> data = new HashMap<>();

        // Big numbers
        long totalUsers = userRepository.count();
        long totalEvents = eventRepository.count();

        // Recent activity (last 7 days)
        LocalDateTime sevenDaysAgo = LocalDateTime.now().minusDays(7);
        long recentEvents = eventRepository.findByCreatedAtAfter(sevenDaysAgo).size();

        // Alerts
        long pendingEvents = eventRepository.findByStatus("pending").size();
        List<String> alerts = pendingEvents > 0 ? List.of(pendingEvents + " events pending approval") : List.of();

        // Recent events
        List<Event> recentEventsList = eventRepository.findTop5ByOrderByCreatedAtDesc();

        // User breakdown by role
        Map<String, Long> userBreakdown = new HashMap<>();
        userBreakdown.put("students", userRepository.findByRole("student").stream().count());
        userBreakdown.put("organizers", userRepository.findByRole("organizer").stream().count());
        userBreakdown.put("admins", userRepository.findByRole("admin").stream().count());

        data.put("big_numbers", Map.of(
            "total_users", totalUsers,
            "total_events", totalEvents
        ));
        data.put("recent_activity", Map.of(
            "events_last_7_days", recentEvents
        ));
        data.put("alerts", alerts);
        data.put("recent_events", recentEventsList);
        data.put("user_breakdown", userBreakdown);

        return data;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User createUser(User user) {
        user.setCreatedAt(LocalDateTime.now());
        user.setUpdatedAt(LocalDateTime.now());
        return userRepository.save(user);
    }

    public void deleteUser(String id) {
        userRepository.deleteById(id);
    }

    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }

    public Event createEvent(Event event) {
        event.setCreatedAt(LocalDateTime.now());
        event.setUpdatedAt(LocalDateTime.now());
        return eventRepository.save(event);
    }

    public Event updateEvent(String id, Event event) {
        Optional<Event> existingEvent = eventRepository.findById(id);
        if (existingEvent.isPresent()) {
            Event updatedEvent = existingEvent.get();
            updatedEvent.setTitle(event.getTitle());
            updatedEvent.setDescription(event.getDescription());
            updatedEvent.setDate(event.getDate());
            updatedEvent.setStartTime(event.getStartTime());
            updatedEvent.setEndTime(event.getEndTime());
            updatedEvent.setLocation(event.getLocation());
            updatedEvent.setCapacity(event.getCapacity());
            updatedEvent.setStatus(event.getStatus());
            updatedEvent.setUpdatedAt(LocalDateTime.now());
            return eventRepository.save(updatedEvent);
        }
        return null;
    }

    public void deleteEvent(String id) {
        eventRepository.deleteById(id);
    }
}

package com.example.collegeeventmanagement.service;

import com.example.collegeeventmanagement.model.Event;
import com.example.collegeeventmanagement.repository.EventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class EventService {

    @Autowired
    private EventRepository eventRepository;

    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }

    public Optional<Event> getEventById(String id) {
        return eventRepository.findById(id);
    }

    public Event createEvent(Event event) {
        return eventRepository.save(event);
    }

    public Event updateEvent(String id, Event eventDetails) {
        Optional<Event> event = eventRepository.findById(id);
        if (event.isPresent()) {
            Event existingEvent = event.get();
            existingEvent.setTitle(eventDetails.getTitle());
            existingEvent.setDescription(eventDetails.getDescription());
            existingEvent.setDate(eventDetails.getDate());
            existingEvent.setStartTime(eventDetails.getStartTime());
            existingEvent.setEndTime(eventDetails.getEndTime());
            existingEvent.setLocation(eventDetails.getLocation());
            existingEvent.setCapacity(eventDetails.getCapacity());
            existingEvent.setStatus(eventDetails.getStatus());
            return eventRepository.save(existingEvent);
        }
        return null;
    }

    public void deleteEvent(String id) {
        eventRepository.deleteById(id);
    }

    public List<Event> getEventsByStatus(String status) {
        return eventRepository.findByStatus(status);
    }
}

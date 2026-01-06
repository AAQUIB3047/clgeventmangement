package com.example.collegeeventmanagement.service;

import com.example.collegeeventmanagement.model.Registration;
import com.example.collegeeventmanagement.repository.RegistrationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class RegistrationService {

    @Autowired
    private RegistrationRepository registrationRepository;

    public List<Registration> getAllRegistrations() {
        return registrationRepository.findAll();
    }

    public Optional<Registration> getRegistrationById(String id) {
        return registrationRepository.findById(id);
    }

    public Registration createRegistration(Registration registration) {
        return registrationRepository.save(registration);
    }

    public Registration updateRegistration(String id, Registration registrationDetails) {
        Optional<Registration> registration = registrationRepository.findById(id);
        if (registration.isPresent()) {
            Registration existingRegistration = registration.get();
            existingRegistration.setStatus(registrationDetails.getStatus());
            return registrationRepository.save(existingRegistration);
        }
        return null;
    }

    public void deleteRegistration(String id) {
        registrationRepository.deleteById(id);
    }

    public List<Registration> getRegistrationsByUser(String userId) {
        return registrationRepository.findByUserId(userId);
    }

    public List<Registration> getRegistrationsByEvent(String eventId) {
        return registrationRepository.findByEventId(eventId);
    }

    public List<Registration> getRegistrationsByStatus(String status) {
        return registrationRepository.findByStatus(status);
    }
}

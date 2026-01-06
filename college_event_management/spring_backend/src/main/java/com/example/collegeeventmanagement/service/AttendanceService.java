package com.example.collegeeventmanagement.service;

import com.example.collegeeventmanagement.model.Attendance;
import com.example.collegeeventmanagement.repository.AttendanceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class AttendanceService {

    @Autowired
    private AttendanceRepository attendanceRepository;

    public List<Attendance> getAllAttendances() {
        return attendanceRepository.findAll();
    }

    public Optional<Attendance> getAttendanceById(String id) {
        return attendanceRepository.findById(id);
    }

    public Attendance createAttendance(Attendance attendance) {
        attendance.setCreatedAt(LocalDateTime.now());
        attendance.setUpdatedAt(LocalDateTime.now());
        return attendanceRepository.save(attendance);
    }

    public Attendance updateAttendance(String id, Attendance attendanceDetails) {
        Optional<Attendance> attendance = attendanceRepository.findById(id);
        if (attendance.isPresent()) {
            Attendance existingAttendance = attendance.get();
            existingAttendance.setCheckedIn(attendanceDetails.isCheckedIn());
            existingAttendance.setCheckInTime(attendanceDetails.getCheckInTime());
            existingAttendance.setNotes(attendanceDetails.getNotes());
            existingAttendance.setUpdatedAt(LocalDateTime.now());
            return attendanceRepository.save(existingAttendance);
        }
        return null;
    }

    public void deleteAttendance(String id) {
        attendanceRepository.deleteById(id);
    }

    public List<Attendance> getAttendancesByRegistration(String registrationId) {
        return attendanceRepository.findByRegistrationId(registrationId);
    }

    public List<Attendance> getAttendancesByEvent(String eventId) {
        return attendanceRepository.findByEventId(eventId);
    }
}

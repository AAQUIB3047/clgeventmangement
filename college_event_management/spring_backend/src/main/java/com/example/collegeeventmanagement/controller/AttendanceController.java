package com.example.collegeeventmanagement.controller;

import com.example.collegeeventmanagement.model.Attendance;
import com.example.collegeeventmanagement.service.AttendanceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/attendance")
@CrossOrigin(origins = "*")
public class AttendanceController {

    @Autowired
    private AttendanceService attendanceService;

    @GetMapping
    public ResponseEntity<List<Attendance>> getAllAttendances() {
        List<Attendance> attendances = attendanceService.getAllAttendances();
        return ResponseEntity.ok(attendances);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Attendance> getAttendanceById(@PathVariable String id) {
        Optional<Attendance> attendance = attendanceService.getAttendanceById(id);
        if (attendance.isPresent()) {
            return ResponseEntity.ok(attendance.get());
        }
        return ResponseEntity.notFound().build();
    }

    @PostMapping
    public ResponseEntity<Attendance> createAttendance(@RequestBody Attendance attendance) {
        Attendance createdAttendance = attendanceService.createAttendance(attendance);
        return ResponseEntity.ok(createdAttendance);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Attendance> updateAttendance(@PathVariable String id, @RequestBody Attendance attendanceDetails) {
        Attendance updatedAttendance = attendanceService.updateAttendance(id, attendanceDetails);
        if (updatedAttendance != null) {
            return ResponseEntity.ok(updatedAttendance);
        }
        return ResponseEntity.notFound().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteAttendance(@PathVariable String id) {
        attendanceService.deleteAttendance(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/registration/{registrationId}")
    public ResponseEntity<List<Attendance>> getAttendancesByRegistration(@PathVariable String registrationId) {
        List<Attendance> attendances = attendanceService.getAttendancesByRegistration(registrationId);
        return ResponseEntity.ok(attendances);
    }

    @GetMapping("/event/{eventId}")
    public ResponseEntity<List<Attendance>> getAttendancesByEvent(@PathVariable String eventId) {
        List<Attendance> attendances = attendanceService.getAttendancesByEvent(eventId);
        return ResponseEntity.ok(attendances);
    }
}

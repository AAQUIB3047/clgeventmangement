package com.example.collegeeventmanagement.repository;

import com.example.collegeeventmanagement.model.Attendance;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AttendanceRepository extends MongoRepository<Attendance, String> {
    List<Attendance> findByCheckedIn(boolean checkedIn);
}

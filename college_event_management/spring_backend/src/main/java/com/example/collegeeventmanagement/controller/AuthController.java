package com.example.collegeeventmanagement.controller;

import com.example.collegeeventmanagement.model.User;
import com.example.collegeeventmanagement.service.UserService;
import com.example.collegeeventmanagement.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtil jwtUtil;

    @GetMapping("/login")
    public ResponseEntity<?> getLoginInfo() {
        Map<String, Object> response = new HashMap<>();
        response.put("name", "Login");
        response.put("description", "");
        response.put("renders", Arrays.asList("application/json", "text/html"));
        response.put("parses", Arrays.asList("application/json", "application/x-www-form-urlencoded", "multipart/form-data"));
        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> loginRequest) {
        String username = loginRequest.get("username");
        String password = loginRequest.get("password");

        Optional<User> user = userService.getUserByUsername(username);
        if (user.isPresent() && user.get().getPassword().equals(password)) { // In production, use password encoder
            String token = jwtUtil.generateToken(username, user.get().getRole());
            Map<String, String> response = new HashMap<>();
            response.put("token", token);
            response.put("role", user.get().getRole());
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.status(401).body("Invalid credentials");
    }
}

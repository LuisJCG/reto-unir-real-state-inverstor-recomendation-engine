package net.unir.dtos;

import java.util.List;

public record UserDTO(String id, String username, String passwordHash, List<String> roles) {}
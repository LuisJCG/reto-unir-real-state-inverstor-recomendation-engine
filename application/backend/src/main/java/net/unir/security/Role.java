package net.unir.security;

public enum Role {
    INVESTOR,
    SPONSOR,
    DATA_ANALYST,
    ADMIN;

    public String asString() { return name(); }
}
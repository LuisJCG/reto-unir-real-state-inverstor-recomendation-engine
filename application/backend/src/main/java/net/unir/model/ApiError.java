package net.unir.model;

public class ApiError {
    public String error;
    public String message;
    public ApiError() {}
    public ApiError(String error, String message) {
        this.error = error; this.message = message;
    }
}

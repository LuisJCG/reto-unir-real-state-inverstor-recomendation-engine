package net.unir.model;

import java.util.List;

public class JobStatus {
    public String job_id;
    public String status; // queued | running | succeeded | failed
    public Double progress;
    public List<String> logs;
}

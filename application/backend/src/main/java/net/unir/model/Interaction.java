package net.unir.model;

import java.time.OffsetDateTime;
import java.util.Map;

public class Interaction {
    public String project_id;
    public String type; // view | click | download | favorite | request_info | investment | thumbs_up | thumbs_down
    public Double weight;
    public Map<String, Object> context;
    public OffsetDateTime created_at;
}

package net.unir.model;

import java.util.List;

public class Project {
    public String id;
    public String name;
    public String type;
    public String country;
    public String city;
    public Double lat;
    public Double lon;
    public Double irr;
    public Double cap_rate;
    public Double min_ticket;
    public Double max_ticket;
    public String esg;
    public String sponsor_id;
    public List<String> tags;
    public List<DocumentRef> documents;
    public double[] embedding;
}

package net.unir.model;

import java.util.List;

public class Investor {
    public String id;
    public String segment; // retail | professional | institution
    public String risk_profile; // conservative | moderate | aggressive
    public String horizon; // short | medium | long
    public Double ticket_min;
    public Double ticket_max;
    public List<String> jurisdictions_ok;
    public List<String> cities_pref;
    public Double esg_pref; // 0..1
    public List<String> tags;
    public double[] embedding;
}

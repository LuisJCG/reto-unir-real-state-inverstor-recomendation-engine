package net.unir.model;

import java.util.List;

public class RecommendationItem {
    public String project_id;
    public Double score_total;
    public ScoreComponents components;
    public List<String> why;
}

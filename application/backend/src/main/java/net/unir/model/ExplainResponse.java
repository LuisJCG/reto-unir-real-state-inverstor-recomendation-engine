package net.unir.model;

import java.util.List;

public class ExplainResponse {
    public Data data;
    public static class Data {
        public Double score_total;
        public ScoreComponents components;
        public List<RuleContribution> rules_contributions;
        public List<GraphPath> graph_paths;
        public List<FeatureImportance> features_top;
    }
    public static class RuleContribution {
        public String rule;
        public Double delta;
    }
    public static class GraphPath {
        public String path;
        public Double weight;
    }
    public static class FeatureImportance {
        public String feature;
        public Double importance;
    }
}

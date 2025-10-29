package net.unir.model;

import java.util.List;

public class JobRequest {
    public Pipeline pipeline;
    public static class Pipeline {
        public String graph_name;
        public Projection projection;
        public FastRP fastrp;
        public KNN knn;
    }
    public static class Projection {
        public List<String> nodeLabels;
        public List<String> relationshipTypes;
    }
    public static class FastRP {
        public Integer embeddingDimension;
        public List<Double> iterationWeights;
        public List<String> featureProperties;
    }
    public static class KNN {
        public Integer topK;
        public Double similarityCutoff;
        public String writeRelationshipType;
        public String writeProperty;
    }
}

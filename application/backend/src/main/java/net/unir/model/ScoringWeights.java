package net.unir.model;

import java.util.Map;

public class ScoringWeights {
    public Double alpha;
    public Double beta;
    public Double gamma;
    public Map<String, SegmentOverride> segment_overrides;
    public static class SegmentOverride {
        public Double alpha;
        public Double beta;
        public Double gamma;
    }
}

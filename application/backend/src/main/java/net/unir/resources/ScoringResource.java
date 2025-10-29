package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.ExplainResponse;
import net.unir.model.ScoreComponents;
import net.unir.model.ScoringWeights;

import java.util.Map;

@Path("/scoring")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ScoringResource {

    private static ScoringWeights weights = defaultWeights();

    @GET
    @Path("/weights")
    public Response getWeights() {
        return Response.ok(Map.of("data", weights)).build();
    }

    @PUT
    @Path("/weights")
    public Response putWeights(ScoringWeights w) {
        weights = w;
        return Response.ok(Map.of("data", weights)).build();
    }

    @POST
    @Path("/preview")
    public Response preview(Map<String, String> body) {
        ExplainResponse out = new ExplainResponse();
        out.data = new ExplainResponse.Data();
        out.data.score_total = 0.77;
        ScoreComponents sc = new ScoreComponents();
        sc.embedding_sim = 0.58; sc.rules_score = 0.16; sc.behavioral_boost = 0.03;
        out.data.components = sc;
        return Response.ok(out).build();
    }

    private static ScoringWeights defaultWeights() {
        ScoringWeights w = new ScoringWeights();
        w.alpha = 0.7; w.beta = 0.25; w.gamma = 0.05;
        return w;
    }
}

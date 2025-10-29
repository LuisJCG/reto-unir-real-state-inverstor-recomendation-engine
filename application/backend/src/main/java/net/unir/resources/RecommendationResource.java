package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.ExplainResponse;
import net.unir.model.Meta;
import net.unir.model.RecommendationItem;
import net.unir.model.RecommendationResponse;
import net.unir.model.ScoreComponents;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;


@Path("/recommendations")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class RecommendationResource {

    @GET
    @Path("/investors/{id}")
    public Response recommend(@PathParam("id") String investorId,
                              @QueryParam("limit") @DefaultValue("20") int limit,
                              @QueryParam("offset") @DefaultValue("0") int offset,
                              @QueryParam("fresh") @DefaultValue("false") boolean fresh) {
        RecommendationItem item = new RecommendationItem();
        item.project_id = "proj-789";
        item.score_total = 0.83;
        ScoreComponents sc = new ScoreComponents();
        sc.embedding_sim = 0.62; sc.rules_score = 0.18; sc.behavioral_boost = 0.03;
        item.components = sc;
        item.why = List.of(
            "Coincide con mandato: office en ES, ticket 50k–500k",
            "Similar a proyectos vistos/guardados"
        );
        RecommendationResponse resp = new RecommendationResponse();
        resp.data = List.of(item);
        Meta meta = new Meta();
        meta.offset = offset; meta.limit = limit; meta.generated_at = OffsetDateTime.now().toString();
        resp.meta = meta;
        return Response.ok(resp).build();
    }

    @GET
    @Path("/investors/{id}/projects/{project_id}/explain")
    public Response explain(@PathParam("id") String investorId, @PathParam("project_id") String projectId) {
        ExplainResponse out = new ExplainResponse();
        out.data = new ExplainResponse.Data();
        out.data.score_total = 0.83;
        ScoreComponents sc = new ScoreComponents();
        sc.embedding_sim = 0.62; sc.rules_score = 0.18; sc.behavioral_boost = 0.03;
        out.data.components = sc;
        ExplainResponse.RuleContribution rc1 = new ExplainResponse.RuleContribution();
        rc1.rule = "mandate_match_country"; rc1.delta = 0.06;
        ExplainResponse.RuleContribution rc2 = new ExplainResponse.RuleContribution();
        rc2.rule = "city_preference"; rc2.delta = 0.04;
        out.data.rules_contributions = List.of(rc1, rc2);
        ExplainResponse.GraphPath gp = new ExplainResponse.GraphPath();
        gp.path = "Investor -> viewed -> Project A -> similar_to -> Project B";
        gp.weight = 0.14;
        out.data.graph_paths = List.of(gp);
        ExplainResponse.FeatureImportance fi = new ExplainResponse.FeatureImportance();
        fi.feature = "city=Madrid"; fi.importance = 0.19;
        out.data.features_top = List.of(fi);
        return Response.ok(out).build();
    }

    @POST
    @Path("/investors/{id}/projects/{project_id}/feedback")
    public Response feedback(@PathParam("id") String investorId,
                             @PathParam("project_id") String projectId,
                             Map<String, Object> body) {
        return Response.status(201).entity(Map.of("status","ok","investor_id", investorId, "project_id", projectId)).build();
    }
}

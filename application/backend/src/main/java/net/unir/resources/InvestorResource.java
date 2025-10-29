package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.Interaction;
import net.unir.model.Investor;
import net.unir.model.InvestorUpdate;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;

@Path("/investors")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class InvestorResource {

    @GET
    @Path("/{id}")
    public Response getInvestor(@PathParam("id") String id) {
        Investor inv = new Investor();
        inv.id = id;
        inv.segment = "professional";
        inv.risk_profile = "moderate";
        inv.horizon = "medium";
        inv.ticket_min = 50000d;
        inv.ticket_max = 500000d;
        inv.jurisdictions_ok = List.of("ES","FR");
        inv.cities_pref = List.of("Madrid","Barcelona");
        inv.esg_pref = 0.7;
        inv.tags = List.of("office","LEED");
        return Response.ok(Map.of("data", inv)).build();
    }

    @PUT
    @Path("/{id}")
    public Response upsertInvestor(@PathParam("id") String id, InvestorUpdate body) {
        body.id = id;
        return Response.ok(Map.of("data", body)).build();
    }

    @POST
    @Path("/{id}/interactions")
    public Response postInteraction(@PathParam("id") String id, Interaction interaction) {
        if (interaction.created_at == null) {
            interaction.created_at = OffsetDateTime.now();
        }
        return Response.status(201).entity(Map.of("data", interaction)).build();
    }

    @GET
    @Path("/{id}/history")
    public Response getHistory(@PathParam("id") String id, @QueryParam("limit") @DefaultValue("50") int limit) {
        Interaction i = new Interaction();
        i.project_id = "proj-123";
        i.type = "view";
        i.weight = 1.0;
        i.context = Map.of("source", "feed", "position", 1);
        i.created_at = OffsetDateTime.now();
        return Response.ok(Map.of("data", List.of(i))).build();
    }

    @POST
    @Path("/{id}/favorites")
    public Response addFavorite(@PathParam("id") String id, Map<String, String> body) {
        return Response.status(201).entity(Map.of("status","saved", "project_id", body.get("project_id"))).build();
    }

    @DELETE
    @Path("/{id}/favorites/{project_id}")
    public Response removeFavorite(@PathParam("id") String id, @PathParam("project_id") String projectId) {
        return Response.status(204).build();
    }
}

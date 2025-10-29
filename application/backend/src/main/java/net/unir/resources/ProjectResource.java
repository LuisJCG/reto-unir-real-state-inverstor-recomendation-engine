package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.Meta;
import net.unir.model.PaginatedProjectList;
import net.unir.model.Project;
import net.unir.model.Tag;

import java.util.List;
import java.util.Map;

@Path("/projects")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ProjectResource {

    @GET
    public Response listProjects(@QueryParam("country") String country,
                                 @QueryParam("city") String city,
                                 @QueryParam("type") String type,
                                 @QueryParam("min_ticket") Double minTicket,
                                 @QueryParam("max_ticket") Double maxTicket,
                                 @QueryParam("esg_min") Double esgMin,
                                 @QueryParam("sort") String sort,
                                 @QueryParam("page") @DefaultValue("1") int page,
                                 @QueryParam("limit") @DefaultValue("20") int limit) {
        Project p = sampleProject("proj-789");
        PaginatedProjectList out = new PaginatedProjectList();
        out.data = List.of(p);
        Meta m = new Meta();
        m.page = page; m.limit = limit; m.total = 1; m.offset = 0;
        out.meta = m;
        return Response.ok(out).build();
    }

    @GET
    @Path("/{id}")
    public Response getProject(@PathParam("id") String id) {
        return Response.ok(Map.of("data", sampleProject(id))).build();
    }

    @GET
    @Path("/{id}/similar")
    public Response similar(@PathParam("id") String id, @QueryParam("limit") @DefaultValue("10") int limit) {
        return Response.ok(Map.of("data", List.of(sampleProject("proj-1"), sampleProject("proj-2")))).build();
    }

    @GET
    @Path("/{id}/suggested-tags")
    public Response suggestedTags(@PathParam("id") String id) {
        return Response.ok(Map.of("data", List.of(tag("LEED","esg"), tag("CBD","use_case")))).build();
    }

    @POST
    @Path("/{id}/request-info")
    public Response requestInfo(@PathParam("id") String id) {
        return Response.status(201).entity(Map.of("status","created","project_id", id)).build();
    }

    private static Project sampleProject(String id) {
        Project p = new Project();
        p.id = id;
        p.name = "Oficinas Centro";
        p.type = "office";
        p.country = "ES";
        p.city = "Madrid";
        p.irr = 0.15;
        p.cap_rate = 0.055;
        p.min_ticket = 50000d;
        p.max_ticket = 250000d;
        p.esg = "LEED";
        p.sponsor_id = "s-12";
        p.tags = java.util.List.of("core","CBD");
        return p;
    }

    private static Tag tag(String name, String type) {
        Tag t = new Tag();
        t.id = name.toLowerCase();
        t.name = name;
        t.type = type;
        return t;
    }
}

package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.Tag;

import java.util.List;
import java.util.Map;

@Path("/tags")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class TagResource {

    @GET
    public Response list(@QueryParam("type") String type) {
        Tag t1 = new Tag(); t1.id = "leed"; t1.name = "LEED"; t1.type = "esg";
        Tag t2 = new Tag(); t2.id = "core"; t2.name = "core"; t2.type = "risk";
        return Response.ok(Map.of("data", List.of(t1, t2))).build();
    }
}

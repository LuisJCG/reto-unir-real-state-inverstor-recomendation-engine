package net.unir.resources;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.Map;

@Path("/")
@Produces(MediaType.APPLICATION_JSON)
public class OpsResource {

    @GET
    @Path("/health")
    public Response health() {
        return Response.ok(Map.of("neo4j","up","gds","up","queue","up","latency_ms",42)).build();
    }

    @GET
    @Path("/stats")
    public Response stats() {
        return Response.ok(Map.of("ctr",0.21,"conversion_request_info",0.07,"embeddings_coverage",0.98)).build();
    }
}

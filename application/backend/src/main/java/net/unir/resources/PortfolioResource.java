package net.unir.resources;

import jakarta.annotation.security.RolesAllowed;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.Response;

@Path("/portfolio")
public class PortfolioResource {

  @GET
  @RolesAllowed({ "USER", "ADMIN" })
  public Response mine() {
    return Response.ok("Mis inversiones").build();
  }

  @GET
  @Path("/admin/summary")
  @RolesAllowed("ADMIN")
  public Response adminOnly() {
    return Response.ok("Resumen global (solo ADMIN)").build();
  }
}

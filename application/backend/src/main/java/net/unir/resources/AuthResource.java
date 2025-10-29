package net.unir.resources;

import io.quarkus.security.Authenticated;
import jakarta.annotation.security.PermitAll;
import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.validation.constraints.NotBlank;
import jakarta.ws.rs.BadRequestException;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.List;
import java.util.Map;
import net.unir.dtos.UserDTO;
import net.unir.security.JwtIssuer;
import net.unir.security.Role;
import net.unir.services.UserService;
import org.eclipse.microprofile.jwt.JsonWebToken;

@Path("/auth")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
@Authenticated
public class AuthResource {

    @Inject
    UserService users;

    @Inject
    JwtIssuer jwtIssuer;

    @Inject
    JsonWebToken jwt; // token actual si está autenticado

    record RegisterReq(String username, String password, List<String> roles) {}

    record LoginReq(String username, String password) {}

    @POST
    @Path("/register")
    @RolesAllowed("ADMIN")
    public Response register(RegisterReq req) {
        if (req == null || req.username == null || req.password == null || req.username.isBlank() || req.password.isBlank()) {
            throw new BadRequestException("username/password requeridos");
        }
        if (users.usernameExists(req.username)) {
            return Response.status(Response.Status.CONFLICT).entity(Map.of("error", "USERNAME_TAKEN")).build();
        }
        List<String> roles = (req.roles == null || req.roles.isEmpty()) ? List.of(Role.INVESTOR.asString()) : req.roles;
        for (String r : roles) {
            try {
                Role.valueOf(r);
            } catch (IllegalArgumentException ex) {
                throw new BadRequestException("Rol inválido: " + r);
            }
        }
        UserDTO u = users.createUser(req.username, req.password, roles);
        return Response.status(Response.Status.CREATED).entity(Map.of("id", u.id(), "username", u.username(), "roles", u.roles())).build();
    }

    @POST
    @Path("/login")
    @PermitAll
    public Response login(LoginReq req) {
        if (req == null || req.username() == null || req.password() == null) throw new BadRequestException("username/password requeridos");

        var userOpt = users.findByUsername(req.username());
        if (userOpt.isEmpty() || !users.verifyPassword(req.password(), userOpt.get().passwordHash())) {
            return Response.status(Response.Status.UNAUTHORIZED).entity(Map.of("error", "INVALID_CREDENTIALS")).build();
        }

        var u = userOpt.get();
        String token = jwtIssuer.issue(u.id(), u.username(), u.roles(), "inv-1");

        return Response.ok(Map.of("access_token", token, "token_type", "Bearer", "expires_in", 3600, "username", u.username(), "roles", u.roles(), "investor_id", "inv-1")).build();
    }

    @POST
    @Path("/refresh")
    public Response refresh() {
        // Requiere token válido en Authorization: Bearer ...
        if (jwt == null || jwt.getSubject() == null) {
            return Response.status(Response.Status.UNAUTHORIZED).entity(Map.of("error", "NO_TOKEN")).build();
        }
        // Reutilizamos claims principales
        var username = jwt.getName(); // upn
        @SuppressWarnings("unchecked")
        var roles = (List<String>) (Object) jwt.getGroups().stream().toList();
        var investorId = jwt.getClaim("investor_id") instanceof String s ? s : "inv-1";

        String token = new JwtIssuer().issue(jwt.getSubject(), username, roles, investorId);
        return Response.ok(Map.of("access_token", token, "token_type", "Bearer", "expires_in", 3600)).build();
    }

    @POST
    @Path("/test")
    @PermitAll
    public Response test() {
        return Response.ok("Endpoint /auth/test is working").build();
    }
}

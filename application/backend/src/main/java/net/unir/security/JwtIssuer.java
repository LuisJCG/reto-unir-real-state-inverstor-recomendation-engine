package net.unir.security;
import io.smallrye.jwt.build.Jwt;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import java.time.Instant;
import java.util.List;
import java.util.Set;

@ApplicationScoped
public class JwtIssuer {

  @ConfigProperty(name = "goldwaves.jwt.ttl-seconds", defaultValue = "3600")
  long ttl;

  public String issue(String subject, String username, List<String> roles, String investorId) {
    Instant now = Instant.now();
    return Jwt.issuer("https://goldwaves/auth")
        .subject(subject)
        .upn(username)
        .groups(Set.copyOf(roles))
        .audience("goldwaves-app")
        .issuedAt(now)
        .expiresAt(now.plusSeconds(ttl))
        .claim("investor_id", investorId)
        .sign();
  }
}
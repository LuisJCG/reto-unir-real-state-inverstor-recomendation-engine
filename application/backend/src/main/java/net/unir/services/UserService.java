package net.unir.services;

import io.quarkus.elytron.security.common.BcryptUtil;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.inject.Inject;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import net.unir.dtos.UserDTO;
import net.unir.security.Role;
import org.neo4j.driver.*;

@ApplicationScoped
public class UserService {

    @Inject
    Driver driver;

    private void ensureConstraints() {
        try (Session s = driver.session()) {
            s.executeWrite(tx -> {
                tx.run("CREATE CONSTRAINT user_username_unique IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE");
                tx.run("CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE");
                return null;
            });
        }
    }

    private void seedDefaultUsers() {
        if (!usernameExists("admin")) createUser("admin", "admin123", List.of(Role.ADMIN.asString()));
        if (!usernameExists("analyst")) createUser("analyst", "analyst123", List.of(Role.DATA_ANALYST.asString()));
        if (!usernameExists("sponsor")) createUser("sponsor", "sponsor123", List.of(Role.SPONSOR.asString()));
        if (!usernameExists("investor")) createUser("investor", "investor123", List.of(Role.INVESTOR.asString()));
    }

    void startup(@Observes StartupEvent event) {
        ensureConstraints();
        seedDefaultUsers();
    }

    public Optional<UserDTO> findByUsername(String username) {
        try (Session s = driver.session()) {
            List<org.neo4j.driver.Record> records = s.executeRead(tx -> {
                return tx.run("MATCH (u:User {username: $u}) " + "RETURN u.id AS id, u.username AS username, u.passwordHash AS ph, u.roles AS roles", Values.parameters("u", username)).list();
            });

            if (records.isEmpty()) {
                return Optional.empty();
            }
            org.neo4j.driver.Record rec = records.get(0);
            List<String> roles = rec.containsKey("roles") && !rec.get("roles").isNull() ? rec.get("roles").asList(Value::asString) : List.of();

            return Optional.of(new UserDTO(rec.get("id").asString(), rec.get("username").asString(), rec.get("ph").asString(), roles));
        }
    }

    public boolean usernameExists(String username) {
        try (Session s = driver.session()) {
            var count = s.executeRead(tx -> tx.run("MATCH (u:User {username:$u}) RETURN count(u) AS c", Values.parameters("u", username)).single().get("c").asLong());
            return count > 0;
        }
    }

    public UserDTO createUser(String username, String rawPassword, List<String> roles) {
        String id = UUID.randomUUID().toString();
        String hash = BcryptUtil.bcryptHash(rawPassword);
        try (Session s = driver.session(); Transaction tx = s.beginTransaction()) {
            tx.run("CREATE (u:User {id:$id, username:$u, passwordHash:$ph, roles:$roles})", Values.parameters("id", id, "u", username, "ph", hash, "roles", roles));
            tx.commit();
        }
        return new UserDTO(id, username, hash, roles);
    }

    public boolean verifyPassword(String rawPassword, String hash) {
        return BcryptUtil.matches(rawPassword, hash);
    }
}

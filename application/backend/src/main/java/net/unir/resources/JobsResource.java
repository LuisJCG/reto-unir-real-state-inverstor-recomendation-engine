package net.unir.resources;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import net.unir.model.JobRequest;
import net.unir.model.JobStatus;

import java.util.List;
import java.util.Map;

@Path("/jobs")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class JobsResource {

    @POST
    @Path("/gds/rebuild")
    public Response rebuild(JobRequest request) {
        JobStatus st = new JobStatus();
        st.job_id = "job-abc-123";
        st.status = "queued";
        st.progress = 0.0;
        st.logs = List.of("queued");
        return Response.status(202).entity(Map.of("data", st)).build();
    }

    @GET
    @Path("/{job_id}")
    public Response status(@PathParam("job_id") String jobId) {
        JobStatus st = new JobStatus();
        st.job_id = jobId;
        st.status = "running";
        st.progress = 0.42;
        st.logs = List.of("projection started","fastrp writing embeddings");
        return Response.ok(Map.of("data", st)).build();
    }
}

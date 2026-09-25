package in.rakshagrid.app.data

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface RakshaApi {
    @GET("demo/round1")
    suspend fun getRound1(): Round1Snapshot

    @POST("demo/round1/report-road")
    suspend fun reportRoad(@Body request: RoadReportRequest): Round1Snapshot

    @POST("demo/round1/reset")
    suspend fun resetRound1(): Round1Snapshot

    @POST("demo/round1/reports/{reportId}/review")
    suspend fun reviewReport(
        @Path("reportId") reportId: Int,
        @Body request: ReportReviewRequest,
    ): Round1Snapshot

    @PATCH("demo/round1/shelters/{shelterId}/capacity")
    suspend fun setShelterCapacity(
        @Path("shelterId") shelterId: String,
        @Body request: ShelterCapacityRequest,
    ): Round1Snapshot
}

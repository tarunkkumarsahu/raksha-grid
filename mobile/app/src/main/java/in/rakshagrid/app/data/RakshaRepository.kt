package in.rakshagrid.app.data

class RakshaRepository(private val api: RakshaApi = ApiClient.api) {
    suspend fun snapshot() = api.getRound1()

    suspend fun reportRoad(
        roadId: String,
        reporterRole: String,
        reason: String = "Flooded / blocked",
        gpsVerified: Boolean = true,
        photoAttached: Boolean = true,
        corroborations: Int = 2,
        contradictingReports: Int = 0,
    ) = api.reportRoad(
        RoadReportRequest(
            roadId = roadId,
            reason = reason,
            reporterRole = reporterRole,
            gpsVerified = gpsVerified,
            photoAttached = photoAttached,
            independentCorroborations = corroborations,
            ageMinutes = 1.0,
            contradictingReports = contradictingReports,
        )
    )

    suspend fun reviewReport(reportId: Int, approve: Boolean) =
        api.reviewReport(reportId, ReportReviewRequest(approve))

    suspend fun setShelterCapacity(shelterId: String, capacityRemaining: Int) =
        api.setShelterCapacity(shelterId, ShelterCapacityRequest(capacityRemaining))

    suspend fun reset() = api.resetRound1()
}

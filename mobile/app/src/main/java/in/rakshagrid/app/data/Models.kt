package in.rakshagrid.app.data

import com.google.gson.annotations.SerializedName

data class Round1Snapshot(
    val mode: String,
    val notice: String,
    val version: Int,
    val event: String,
    @SerializedName("blocked_roads") val blockedRoads: List<String> = emptyList(),
    val roads: List<RoadState> = emptyList(),
    val shelters: List<ShelterState> = emptyList(),
    val settlements: Map<String, SettlementState> = emptyMap(),
    @SerializedName("last_report") val lastReport: ReportResult? = null,
    val reports: List<ReportResult> = emptyList(),
    val citizen: CitizenState,
    val responder: ResponderState,
    val officer: OfficerState,
    @SerializedName("report_result") val reportResult: ReportResult? = null,
)

data class RoadState(
    val id: String,
    val source: String,
    val target: String,
    val blocked: Boolean,
)

data class ShelterState(
    val id: String,
    val name: String,
    @SerializedName("capacity_remaining") val capacityRemaining: Int,
)

data class SettlementState(
    val settlement: String,
    @SerializedName("population_exposed") val populationExposed: Int,
    @SerializedName("people_to_evacuate_demo") val peopleToEvacuateDemo: Int,
    @SerializedName("safe_exits_remaining") val safeExitsRemaining: Int,
    @SerializedName("time_to_isolation_minutes") val timeToIsolationMinutes: Double,
    @SerializedName("priority_score") val priorityScore: Double,
    @SerializedName("priority_band") val priorityBand: String,
    val explanation: List<String> = emptyList(),
    @SerializedName("recommended_shelter") val recommendedShelter: String,
    @SerializedName("shelter_id") val shelterId: String?,
    val route: List<String> = emptyList(),
    @SerializedName("travel_minutes") val travelMinutes: Double?,
    @SerializedName("route_risk") val routeRisk: Double?,
    @SerializedName("route_status") val routeStatus: String,
)

data class CitizenState(
    val location: String,
    val risk: String,
    @SerializedName("time_to_isolation_minutes") val timeToIsolationMinutes: Double,
    @SerializedName("recommended_shelter") val recommendedShelter: String,
    val route: List<String> = emptyList(),
    @SerializedName("travel_minutes") val travelMinutes: Double?,
    @SerializedName("route_risk") val routeRisk: Double?,
    @SerializedName("route_status") val routeStatus: String,
    val message: String,
)

data class ResponderState(
    val mission: String,
    val priority: String,
    @SerializedName("population_exposed") val populationExposed: Int,
    @SerializedName("safe_exits_remaining") val safeExitsRemaining: Int,
    @SerializedName("approach_route") val approachRoute: List<String> = emptyList(),
    val message: String,
)

data class OfficerState(
    val settlement: String,
    @SerializedName("priority_score") val priorityScore: Double,
    @SerializedName("priority_band") val priorityBand: String,
    @SerializedName("time_to_isolation_minutes") val timeToIsolationMinutes: Double,
    @SerializedName("safe_exits_remaining") val safeExitsRemaining: Int,
    @SerializedName("recommended_shelter") val recommendedShelter: String,
    @SerializedName("blocked_roads") val blockedRoads: List<String> = emptyList(),
    val explanation: List<String> = emptyList(),
    @SerializedName("priority_settlements") val prioritySettlements: List<SettlementState> = emptyList(),
    @SerializedName("pending_reports") val pendingReports: List<ReportResult> = emptyList(),
)

data class ReportResult(
    @SerializedName("report_id") val reportId: Int,
    @SerializedName("road_id") val roadId: String,
    val reason: String,
    val confidence: Double,
    val state: String,
    val accepted: Boolean,
    val status: String,
    val evidence: List<String> = emptyList(),
    @SerializedName("reviewed_by") val reviewedBy: String? = null,
)

data class RoadReportRequest(
    @SerializedName("road_id") val roadId: String,
    val reason: String,
    @SerializedName("reporter_role") val reporterRole: String,
    @SerializedName("gps_verified") val gpsVerified: Boolean,
    @SerializedName("photo_attached") val photoAttached: Boolean,
    @SerializedName("independent_corroborations") val independentCorroborations: Int,
    @SerializedName("age_minutes") val ageMinutes: Double,
    @SerializedName("contradicting_reports") val contradictingReports: Int,
)

data class ReportReviewRequest(val approve: Boolean)

data class ShelterCapacityRequest(
    @SerializedName("capacity_remaining") val capacityRemaining: Int,
)

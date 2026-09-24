package in.rakshagrid.app.ui

import android.os.Handler
import android.os.Looper
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

enum class UserRole(val label: String) {
    CITIZEN("Citizen"),
    RESPONDER("Responder"),
    OFFICER("Officer")
}

// 10.0.2.2 maps an Android EMULATOR to the host computer.
// On a physical phone, enter your computer's LAN IP address instead.
private const val EMULATOR_API = "http://10.0.2.2:8000"

private fun requestJson(baseUrl: String, path: String, body: JSONObject? = null): JSONObject {
    val connection = URL(baseUrl.trimEnd('/') + path).openConnection() as HttpURLConnection
    try {
        connection.connectTimeout = 3000
        connection.readTimeout = 3000
        if (body != null) {
            connection.requestMethod = "POST"
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json")
            connection.outputStream.use {
                it.write(body.toString().toByteArray(Charsets.UTF_8))
            }
        }
        val code = connection.responseCode
        val stream = if (code in 200..299) connection.inputStream else connection.errorStream
        val response = stream?.bufferedReader()?.use { it.readText() } ?: ""
        if (code !in 200..299) throw IllegalStateException("API $code: $response")
        return JSONObject(response)
    } finally {
        connection.disconnect()
    }
}

private fun JSONArray.objects(): List<JSONObject> =
    (0 until length()).map { getJSONObject(it) }

private fun JSONObject?.array(name: String): List<JSONObject> =
    this?.optJSONArray(name)?.objects() ?: emptyList()

@Composable
fun RakshaGridApp() {
    var role by remember { mutableStateOf(UserRole.CITIZEN) }
    var apiUrl by remember { mutableStateOf(EMULATOR_API) }
    var snapshot by remember { mutableStateOf<JSONObject?>(null) }
    var networkError by remember { mutableStateOf<String?>(null) }
    var actionMessage by remember { mutableStateOf("") }
    var selectedRoad by remember { mutableStateOf("BR-12") }
    val mainThread = remember { Handler(Looper.getMainLooper()) }

    // Polling is enough for the Round 1 demo. Realtime sockets are a later milestone.
    DisposableEffect(apiUrl) {
        val pool = Executors.newSingleThreadScheduledExecutor()
        val future = pool.scheduleAtFixedRate({
            try {
                val next = requestJson(apiUrl, "/demo/state")
                mainThread.post {
                    snapshot = next
                    networkError = null
                }
            } catch (e: Exception) {
                mainThread.post { networkError = e.message ?: "Cannot connect to backend" }
            }
        }, 0, 2, TimeUnit.SECONDS)
        onDispose {
            future.cancel(true)
            pool.shutdownNow()
        }
    }

    fun perform(path: String, data: JSONObject, label: String) {
        actionMessage = "Submitting..."
        // Never perform network I/O on the Compose/UI thread.
        val endpoint = apiUrl
        Thread {
            try {
                val result = requestJson(endpoint, path, data)
                mainThread.post {
                    snapshot = result.optJSONObject("state") ?: result
                    actionMessage = label
                }
            } catch (e: Exception) {
                mainThread.post { actionMessage = "Request failed: ${e.message}" }
            }
        }.start()
    }

    MaterialTheme {
        Surface(Modifier.fillMaxSize()) {
            Scaffold { padding ->
                Column(
                    Modifier.padding(padding).verticalScroll(rememberScrollState())
                        .padding(18.dp).fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    Text("RAKSHA GRID", style = MaterialTheme.typography.headlineMedium)
                    Text("From warning to coordinated action.")
                    Text(
                        "SIMULATION ONLY — fictional villages and road-failure times. " +
                            "Routes are not verified safe for travel.",
                        color = MaterialTheme.colorScheme.error
                    )
                    OutlinedTextField(
                        value = apiUrl,
                        onValueChange = { apiUrl = it },
                        label = { Text("Backend URL (emulator: 10.0.2.2)") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    networkError?.let {
                        Text("Connection: $it", color = MaterialTheme.colorScheme.error)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        UserRole.entries.forEach { nextRole ->
                            Button(onClick = { role = nextRole },
                                enabled = role != nextRole) {
                                Text(nextRole.label, style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                    if (snapshot == null) {
                        Text("Connecting to RAKSHA Grid backend...")
                    } else {
                        val state = snapshot!!
                        val villages = state.array("priority_settlements")
                        val rampur = villages.firstOrNull { it.optString("id") == "rampur" }
                        when (role) {
                            UserRole.CITIZEN -> CitizenView(rampur)
                            UserRole.RESPONDER -> ResponderView(
                                rampur = rampur,
                                roads = state.array("roads"),
                                selectedRoad = selectedRoad,
                                onRoadSelected = { selectedRoad = it },
                                onReport = {
                                    val report = JSONObject()
                                        .put("road_id", selectedRoad)
                                        .put("reporter_role", "responder")
                                        .put("observation",
                                            if (selectedRoad == "BR-12") "bridge_submerged"
                                            else "road_flooded")
                                    perform("/demo/reports", report, "Report sent for officer review.")
                                }
                            )
                            UserRole.OFFICER -> OfficerView(
                                villages = villages,
                                reports = state.array("reports"),
                                onReview = { id, decision ->
                                    perform("/demo/reports/$id/review",
                                        JSONObject().put("reviewer_role", "officer")
                                            .put("decision", decision),
                                        "Report reviewed; situation updated.")
                                }
                            )
                        }
                        Text("Shared backend state: v${state.optInt("version")}")
                    }
                    if (actionMessage.isNotBlank()) {
                        Text(actionMessage, color = MaterialTheme.colorScheme.primary)
                    }
                    Spacer(Modifier.height(20.dp))
                    Text(
                        "Demo-only role selector. Officer actions have no authentication. " +
                            "Do not use this app for real emergency response.",
                        style = MaterialTheme.typography.bodySmall
                    )
                }
            }
        }
    }
}

@Composable
private fun CitizenView(rampur: JSONObject?) {
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("CITIZEN · RAMPUR (FICTIONAL)",
                style = MaterialTheme.typography.labelLarge)
            if (rampur == null) { Text("No settlement data."); return@Column }
            val tti = rampur.opt("time_to_isolation_minutes")
            val ttiText = if (tti == JSONObject.NULL) "Unknown" else "$tti min"
            Text("Modelled Time to Isolation: $ttiText",
                style = MaterialTheme.typography.titleLarge)
            Text("Currently usable exits in demo: ${rampur.optInt("usable_exits")}")
            val route = rampur.optJSONObject("recommended_route")
            if (route != null) {
                Text("Provisional destination: ${route.optString("shelter_name")}",
                    style = MaterialTheme.typography.titleMedium)
                Text(route.optJSONArray("path_labels")?.objectsAsText() ?: "")
                Text("Modelled travel time: ${route.optDouble("travel_minutes")} min")
            } else {
                Text("NO MODELLED ROUTE REMAINS. Follow official instructions and " +
                    "do not attempt to use blocked roads.",
                    color = MaterialTheme.colorScheme.error)
            }
        }
    }
}

private fun JSONArray.objectsAsText(): String =
    (0 until length()).joinToString(" → ") { getString(it) }

@Composable
private fun ResponderView(
    rampur: JSONObject?,
    roads: List<JSONObject>,
    selectedRoad: String,
    onRoadSelected: (String) -> Unit,
    onReport: () -> Unit
) {
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("RESPONDER · FIELD REPORT", style = MaterialTheme.typography.titleLarge)
            Text("Current mission: Rampur (fictional)")
            val route = rampur?.optJSONObject("recommended_route")
            Text("Approach: " + (route?.optJSONArray("path_labels")?.objectsAsText()
                ?: "No modelled route available"))
            Text("Choose simulated road to report:")
            roads.forEach { road ->
                Button(
                    onClick = { onRoadSelected(road.getString("id")) },
                    enabled = selectedRoad != road.getString("id")
                ) { Text(road.getString("id")) }
            }
            Text("Selected: $selectedRoad")
            Button(onClick = onReport) { Text("Submit road blockage report") }
            Text("The officer must review this report before the road is removed.")
        }
    }
}

@Composable
private fun OfficerView(
    villages: List<JSONObject>,
    reports: List<JSONObject>,
    onReview: (String, String) -> Unit
) {
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("OFFICER · DEMO COMMAND", style = MaterialTheme.typography.titleLarge)
            Text("Modelled settlement priorities")
            villages.forEach { village ->
                Text("${village.optString("name")}: priority " +
                    "${village.optDouble("priority_score")} · " +
                    "${village.optInt("usable_exits")} exit(s)")
            }
            Text("Field reports", style = MaterialTheme.typography.titleMedium)
            if (reports.isEmpty()) Text("No reports received.")
            reports.forEach { report ->
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("${report.optString("id")}: ${report.optString("road_id")} · " +
                        report.optString("status"))
                    if (report.optString("status") == "pending_officer_review") {
                        Button(onClick = {
                            onReview(report.getString("id"), "confirm_blocked")
                        }) { Text("Confirm blockage") }
                        Button(onClick = {
                            onReview(report.getString("id"), "reject_report")
                        }) { Text("Reject report") }
                    }
                }
            }
        }
    }
}

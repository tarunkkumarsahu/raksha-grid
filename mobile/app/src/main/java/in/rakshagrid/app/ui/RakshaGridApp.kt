package in.rakshagrid.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

enum class UserRole(val label: String) {
    CITIZEN("Citizen"),
    RESPONDER("Responder"),
    OFFICER("Officer")
}

@Composable
fun RakshaGridApp() {
    var role by remember { mutableStateOf(UserRole.CITIZEN) }

    MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            Scaffold { padding ->
                Column(
                    modifier = Modifier
                        .padding(padding)
                        .padding(20.dp)
                        .fillMaxSize(),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Text("RAKSHA Grid", style = MaterialTheme.typography.headlineMedium)
                    Text("From disaster warning to coordinated action.")
                    RoleSwitcher(selected = role, onSelect = { role = it })
                    when (role) {
                        UserRole.CITIZEN -> CitizenHome()
                        UserRole.RESPONDER -> ResponderHome()
                        UserRole.OFFICER -> OfficerHome()
                    }
                }
            }
        }
    }
}

@Composable
private fun RoleSwitcher(selected: UserRole, onSelect: (UserRole) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        UserRole.entries.forEach { role ->
            Button(onClick = { onSelect(role) }, enabled = role != selected) {
                Text(role.label)
            }
        }
    }
}

@Composable
private fun CitizenHome() {
    StatusCard(
        title = "HIGH FLOOD RISK",
        lines = listOf(
            "Location: Rampur (demo scenario)",
            "Time to Isolation: 37 min",
            "Recommended shelter: Shelter B",
            "Safe route: available",
            "Data mode: SIMULATION"
        ),
        action = "TAKE ME TO SAFETY"
    )
}

@Composable
private fun ResponderHome() {
    StatusCard(
        title = "MISSION: RAMPUR",
        lines = listOf(
            "Priority: CRITICAL",
            "Population exposed: 1,840",
            "Safe approach: Corridor R12",
            "Field reporting: next milestone",
            "Data mode: SIMULATION"
        ),
        action = "START MISSION"
    )
}

@Composable
private fun OfficerHome() {
    StatusCard(
        title = "DISTRICT RESPONSE OVERVIEW",
        lines = listOf(
            "Top priority: Rampur",
            "Reason: one viable exit remaining",
            "TTI: 37 min",
            "Dynamic map: next milestone",
            "Data mode: SIMULATION"
        ),
        action = "OPEN PRIORITY QUEUE"
    )
}

@Composable
private fun StatusCard(title: String, lines: List<String>, action: String) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(title, style = MaterialTheme.typography.titleLarge)
            Spacer(Modifier.height(12.dp))
            lines.forEach { Text(it) }
            Spacer(Modifier.height(20.dp))
            Button(onClick = { }) {
                Text(action)
            }
        }
    }
}

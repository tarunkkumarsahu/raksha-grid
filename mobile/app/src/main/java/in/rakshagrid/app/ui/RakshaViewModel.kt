package in.rakshagrid.app.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import in.rakshagrid.app.data.RakshaRepository
import in.rakshagrid.app.data.Round1Snapshot
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import retrofit2.HttpException
import java.io.IOException

data class RakshaUiState(
    val snapshot: Round1Snapshot? = null,
    val loading: Boolean = true,
    val actionInProgress: Boolean = false,
    val error: String? = null,
)

class RakshaViewModel(
    private val repository: RakshaRepository = RakshaRepository(),
) : ViewModel() {
    var uiState by mutableStateOf(RakshaUiState())
        private set

    init {
        viewModelScope.launch {
            refreshInternal(showSpinner = true)
            while (isActive) {
                delay(3_000)
                refreshInternal(showSpinner = false)
            }
        }
    }

    fun refresh() {
        viewModelScope.launch { refreshInternal(showSpinner = uiState.snapshot == null) }
    }

    fun submitCitizenRoadReport(roadId: String = "B12") {
        runAction {
            repository.reportRoad(
                roadId = roadId,
                reporterRole = "citizen",
                reason = "Citizen reports road blocked by floodwater",
                corroborations = 0,
            )
        }
    }

    fun reportRoadAsResponseTeam(roadId: String) {
        runAction {
            repository.reportRoad(
                roadId = roadId,
                reporterRole = "responder",
                reason = "Response team confirms flooded / blocked road",
            )
        }
    }

    fun reviewReport(reportId: Int, approve: Boolean) {
        runAction { repository.reviewReport(reportId, approve) }
    }

    fun setShelterCapacity(shelterId: String, capacityRemaining: Int) {
        runAction { repository.setShelterCapacity(shelterId, capacityRemaining) }
    }

    fun resetDemo() {
        runAction { repository.reset() }
    }

    private fun runAction(call: suspend () -> Round1Snapshot) {
        viewModelScope.launch {
            uiState = uiState.copy(actionInProgress = true, error = null)
            try {
                uiState = uiState.copy(
                    snapshot = call(),
                    loading = false,
                    actionInProgress = false,
                    error = null,
                )
            } catch (error: Exception) {
                uiState = uiState.copy(
                    actionInProgress = false,
                    error = error.toUiMessage(),
                )
            }
        }
    }

    private suspend fun refreshInternal(showSpinner: Boolean) {
        if (showSpinner) uiState = uiState.copy(loading = true, error = null)
        try {
            val latest = repository.snapshot()
            if (uiState.snapshot?.version != latest.version) {
                uiState = uiState.copy(snapshot = latest, loading = false, error = null)
            } else if (showSpinner) {
                uiState = uiState.copy(loading = false, error = null)
            }
        } catch (error: Exception) {
            uiState = uiState.copy(
                loading = false,
                error = if (uiState.snapshot == null) error.toUiMessage() else uiState.error,
            )
        }
    }
}

private fun Exception.toUiMessage(): String = when (this) {
    is IOException -> "Cannot reach RAKSHA backend. Check server, Wi-Fi and API base URL."
    is HttpException -> "Backend error ${code()}: ${message()}"
    else -> message ?: "Unexpected backend error."
}

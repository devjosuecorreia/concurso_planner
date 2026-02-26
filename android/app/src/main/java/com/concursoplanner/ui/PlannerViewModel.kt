package com.concursoplanner.ui

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.concursoplanner.data.AppDatabase
import com.concursoplanner.data.PlannerRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.time.LocalDate

data class DashboardUiState(
    val weekSessions: Int = 0,
    val weekMinutes: Int = 0,
    val pendingRevisionsToday: Int = 0,
    val accuracyRate: Double = 0.0
)

class PlannerViewModel(
    private val repository: PlannerRepository
) : ViewModel() {

    val dashboard: StateFlow<DashboardUiState> = combine(
        repository.weekSessions(),
        repository.weekMinutes(),
        repository.pendingRevisionsToday(LocalDate.now()),
        repository.accuracyRate()
    ) { weekSessions, weekMinutes, pending, accuracy ->
        DashboardUiState(
            weekSessions = weekSessions,
            weekMinutes = weekMinutes,
            pendingRevisionsToday = pending,
            accuracyRate = accuracy
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), DashboardUiState())

    fun seedDemoData() {
        viewModelScope.launch {
            repository.createDemoSeed()
        }
    }
}

class PlannerViewModelFactory(private val app: Application) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        val dao = AppDatabase.get(app).plannerDao()
        val repository = PlannerRepository(dao)
        @Suppress("UNCHECKED_CAST")
        return PlannerViewModel(repository) as T
    }
}

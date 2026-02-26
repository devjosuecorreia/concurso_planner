package com.concursoplanner

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.concursoplanner.notifications.RevisionReminderWorker
import com.concursoplanner.ui.PlannerViewModel
import com.concursoplanner.ui.PlannerViewModelFactory
import kotlinx.coroutines.launch
import java.util.concurrent.TimeUnit

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enqueueDailyRevisionReminder()

        setContent {
            MaterialTheme {
                val vm: PlannerViewModel = viewModel(factory = PlannerViewModelFactory(application))
                PlannerApp(vm)
            }
        }
    }

    private fun enqueueDailyRevisionReminder() {
        val request = PeriodicWorkRequestBuilder<RevisionReminderWorker>(24, TimeUnit.HOURS).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            RevisionReminderWorker.WORK_NAME,
            ExistingPeriodicWorkPolicy.UPDATE,
            request
        )
    }
}

@Composable
private fun PlannerApp(vm: PlannerViewModel) {
    val scope = rememberCoroutineScope()
    val stats by vm.dashboard.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Concurso Planner (Android)") }) }
    ) { padding ->
        DashboardContent(
            stats = stats,
            padding = padding,
            onSeedData = { scope.launch { vm.seedDemoData() } }
        )
    }
}

@Composable
private fun DashboardContent(
    stats: com.concursoplanner.ui.DashboardUiState,
    padding: PaddingValues,
    onSeedData: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(padding)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Sessões realizadas na semana: ${stats.weekSessions}")
        Text("Tempo estudado na semana: ${stats.weekMinutes} min")
        Text("Revisões pendentes hoje: ${stats.pendingRevisionsToday}")
        Text("Taxa média de acertos: ${"%.1f".format(stats.accuracyRate)}%")
        Button(onClick = onSeedData) {
            Text("Inserir dados de exemplo")
        }
        Text(
            "Após cada sessão, o usuário deve registrar um relato detalhado " +
                "(recall/ensinar a si mesmo), alimentando o progresso semanal."
        )
    }
}

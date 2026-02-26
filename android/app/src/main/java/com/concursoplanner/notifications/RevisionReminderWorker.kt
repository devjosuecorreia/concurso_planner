package com.concursoplanner.notifications

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.concursoplanner.data.AppDatabase
import kotlinx.coroutines.flow.first
import java.time.LocalDate

class RevisionReminderWorker(
    appContext: Context,
    params: WorkerParameters
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val count = AppDatabase.get(applicationContext)
            .plannerDao()
            .pendingRevisions(LocalDate.now())
            .first()

        if (count > 0) showNotification(count)

        return Result.success()
    }

    private fun showNotification(pending: Int) {
        val channelId = CHANNEL_ID
        val nm = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        nm.createNotificationChannel(
            NotificationChannel(
                channelId,
                "Revisões de estudo",
                NotificationManager.IMPORTANCE_DEFAULT
            )
        )

        if (ContextCompat.checkSelfPermission(
                applicationContext,
                Manifest.permission.POST_NOTIFICATIONS
            ) != PackageManager.PERMISSION_GRANTED
        ) return

        val notification = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("Revisões pendentes hoje")
            .setContentText("Você tem $pending revisões para fazer. Bora estudar?")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()

        NotificationManagerCompat.from(applicationContext).notify(1001, notification)
    }

    companion object {
        const val WORK_NAME = "daily_revision_reminder"
        private const val CHANNEL_ID = "revision_channel"
    }
}

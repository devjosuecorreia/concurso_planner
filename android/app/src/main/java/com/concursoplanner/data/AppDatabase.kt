package com.concursoplanner.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverter
import androidx.room.TypeConverters
import java.time.LocalDate
import java.time.LocalDateTime

class Converters {
    @TypeConverter fun localDateToString(value: LocalDate?): String? = value?.toString()
    @TypeConverter fun stringToLocalDate(value: String?): LocalDate? = value?.let(LocalDate::parse)

    @TypeConverter fun localDateTimeToString(value: LocalDateTime?): String? = value?.toString()
    @TypeConverter fun stringToLocalDateTime(value: String?): LocalDateTime? = value?.let(LocalDateTime::parse)
}

@Database(
    entities = [
        DisciplinaEntity::class,
        AssuntoEntity::class,
        MaterialEntity::class,
        SessaoEntity::class,
        RevisaoEntity::class,
        FlashcardEntity::class,
        PracticeLogEntity::class,
        EventoEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun plannerDao(): PlannerDao

    companion object {
        @Volatile private var instance: AppDatabase? = null

        fun get(context: Context): AppDatabase = instance ?: synchronized(this) {
            instance ?: Room.databaseBuilder(
                context.applicationContext,
                AppDatabase::class.java,
                "concurso_planner_android.db"
            ).build().also { instance = it }
        }
    }
}

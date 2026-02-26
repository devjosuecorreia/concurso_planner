package com.concursoplanner.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
import java.time.LocalDate

@Dao
interface PlannerDao {
    @Insert
    suspend fun insertDisciplina(disciplina: DisciplinaEntity): Long

    @Insert
    suspend fun insertAssunto(assunto: AssuntoEntity): Long

    @Insert
    suspend fun insertMaterial(material: MaterialEntity): Long

    @Insert
    suspend fun insertSessao(sessao: SessaoEntity): Long

    @Insert
    suspend fun insertRevisoes(revisoes: List<RevisaoEntity>)

    @Insert
    suspend fun insertPracticeLog(log: PracticeLogEntity)

    @Query("SELECT COUNT(*) FROM sessoes WHERE fim IS NOT NULL AND date(inicio) >= date('now', '-6 day')")
    fun weekSessions(): Flow<Int>

    @Query("SELECT COALESCE(SUM(strftime('%s', fim) - strftime('%s', inicio))/60, 0) FROM sessoes WHERE fim IS NOT NULL AND date(inicio) >= date('now', '-6 day')")
    fun weekMinutes(): Flow<Int>

    @Query("SELECT COUNT(*) FROM revisoes WHERE agendadaPara <= :today AND realizada = 0")
    fun pendingRevisions(today: LocalDate): Flow<Int>

    @Query("SELECT COALESCE(AVG((100.0 * corretas) / NULLIF(resolvidas, 0)), 0) FROM practice_logs")
    fun accuracyRate(): Flow<Double>

    @Query("SELECT COUNT(*) FROM disciplinas")
    suspend fun totalDisciplinas(): Int
}

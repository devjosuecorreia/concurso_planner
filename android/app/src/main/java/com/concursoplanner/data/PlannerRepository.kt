package com.concursoplanner.data

import com.concursoplanner.domain.SpacedRepetition
import kotlinx.coroutines.flow.Flow
import java.time.LocalDate
import java.time.LocalDateTime

class PlannerRepository(private val dao: PlannerDao) {
    fun weekSessions(): Flow<Int> = dao.weekSessions()
    fun weekMinutes(): Flow<Int> = dao.weekMinutes()
    fun pendingRevisionsToday(today: LocalDate): Flow<Int> = dao.pendingRevisions(today)
    fun accuracyRate(): Flow<Double> = dao.accuracyRate()

    suspend fun createMaterialWithReviews(
        titulo: String,
        tipo: String,
        disciplinaId: Long,
        assuntoId: Long,
        revisoesDesejadas: Int,
        uriArquivo: String?
    ) {
        val materialId = dao.insertMaterial(
            MaterialEntity(
                titulo = titulo,
                tipo = tipo,
                disciplinaId = disciplinaId,
                assuntoId = assuntoId,
                revisoesDesejadas = revisoesDesejadas,
                uriArquivo = uriArquivo
            )
        )

        val revisoes = SpacedRepetition.schedule(LocalDate.now(), revisoesDesejadas).map {
            RevisaoEntity(
                materialId = materialId,
                disciplinaId = disciplinaId,
                assuntoId = assuntoId,
                agendadaPara = it
            )
        }
        dao.insertRevisoes(revisoes)
    }

    suspend fun finishStudySession(
        disciplinaId: Long,
        assuntoId: Long,
        materialId: Long?,
        startedAt: LocalDateTime,
        relato: String,
        resolvidas: Int,
        corretas: Int
    ) {
        require(relato.length >= 30) {
            "Relato final deve ser detalhado para validar técnica de recall."
        }

        dao.insertSessao(
            SessaoEntity(
                tipo = "estudo",
                disciplinaId = disciplinaId,
                assuntoId = assuntoId,
                materialId = materialId,
                inicio = startedAt,
                fim = LocalDateTime.now(),
                relato = relato,
                questoesResolvidas = resolvidas,
                questoesCorretas = corretas
            )
        )

        dao.insertPracticeLog(
            PracticeLogEntity(
                data = LocalDate.now(),
                disciplinaId = disciplinaId,
                assuntoId = assuntoId,
                resolvidas = resolvidas,
                corretas = corretas
            )
        )
    }

    suspend fun createDemoSeed() {
        if (dao.totalDisciplinas() > 0) return

        val disciplinaId = dao.insertDisciplina(DisciplinaEntity(nome = "Direito Constitucional"))
        val assuntoId = dao.insertAssunto(AssuntoEntity(disciplinaId = disciplinaId, nome = "Controle de Constitucionalidade"))

        createMaterialWithReviews(
            titulo = "Aula 01 + PDF",
            tipo = "pdf",
            disciplinaId = disciplinaId,
            assuntoId = assuntoId,
            revisoesDesejadas = 5,
            uriArquivo = null
        )

        finishStudySession(
            disciplinaId = disciplinaId,
            assuntoId = assuntoId,
            materialId = null,
            startedAt = LocalDateTime.now().minusMinutes(90),
            relato = "Revisei competências do STF, ADI/ADC/ADPF, legitimados e efeitos temporais, explicando em voz alta.",
            resolvidas = 20,
            corretas = 16
        )
    }
}

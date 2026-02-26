package com.concursoplanner.data

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey
import java.time.LocalDate
import java.time.LocalDateTime

@Entity(tableName = "disciplinas")
data class DisciplinaEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val nome: String
)

@Entity(
    tableName = "assuntos",
    foreignKeys = [ForeignKey(
        entity = DisciplinaEntity::class,
        parentColumns = ["id"],
        childColumns = ["disciplinaId"],
        onDelete = ForeignKey.CASCADE
    )],
    indices = [Index("disciplinaId")]
)
data class AssuntoEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val disciplinaId: Long,
    val nome: String
)

@Entity(tableName = "materiais", indices = [Index("assuntoId")])
data class MaterialEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val titulo: String,
    val tipo: String,
    val uriArquivo: String?,
    val disciplinaId: Long,
    val assuntoId: Long,
    val revisoesDesejadas: Int,
    val criadoEm: LocalDateTime = LocalDateTime.now()
)

@Entity(tableName = "sessoes", indices = [Index("assuntoId")])
data class SessaoEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val tipo: String,
    val disciplinaId: Long,
    val assuntoId: Long,
    val materialId: Long?,
    val inicio: LocalDateTime = LocalDateTime.now(),
    val fim: LocalDateTime?,
    val relato: String,
    val questoesResolvidas: Int = 0,
    val questoesCorretas: Int = 0
)

@Entity(tableName = "revisoes", indices = [Index("agendadaPara")])
data class RevisaoEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val materialId: Long,
    val disciplinaId: Long,
    val assuntoId: Long,
    val agendadaPara: LocalDate,
    val realizada: Boolean = false,
    val sessaoId: Long? = null
)

@Entity(tableName = "flashcards", indices = [Index("assuntoId")])
data class FlashcardEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val disciplinaId: Long,
    val assuntoId: Long,
    val deck: String,
    val dificuldade: String,
    val frente: String,
    val verso: String,
    val easeFactor: Double = 2.5,
    val intervaloDias: Int = 0,
    val repeticoes: Int = 0,
    val dueDate: LocalDate = LocalDate.now()
)

@Entity(tableName = "practice_logs", indices = [Index("data")])
data class PracticeLogEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val data: LocalDate,
    val disciplinaId: Long,
    val assuntoId: Long,
    val resolvidas: Int,
    val corretas: Int
)

@Entity(tableName = "eventos", indices = [Index("inicio")])
data class EventoEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val titulo: String,
    val tipo: String,
    val inicio: LocalDateTime,
    val fim: LocalDateTime?,
    val descricao: String = ""
)

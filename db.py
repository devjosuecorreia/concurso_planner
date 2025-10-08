from sqlalchemy import create_engine, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import datetime as dt
import os

DB_PATH = os.environ.get("DB_PATH") or os.path.join(os.path.dirname(__file__), "studyplanner.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), unique=True)

    assuntos: Mapped[list["Assunto"]] = relationship(back_populates="disciplina")

class Assunto(Base):
    __tablename__ = "assuntos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))

    disciplina: Mapped["Disciplina"] = relationship(back_populates="assuntos")

class Material(Base):
    __tablename__ = "materiais"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(300))
    tipo: Mapped[str] = mapped_column(String(50))  # video, pdf, docx, audio, texto
    filepath: Mapped[str] = mapped_column(String(500), nullable=True)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    assunto_id: Mapped[int] = mapped_column(ForeignKey("assuntos.id"))
    notas: Mapped[str] = mapped_column(Text, default="")
    criado_em: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.now)

class Sessao(Base):
    __tablename__ = "sessoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(50))  # estudo | revisao
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    assunto_id: Mapped[int] = mapped_column(ForeignKey("assuntos.id"))
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais.id"), nullable=True)
    data_inicio: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.now)
    data_fim: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    relato_texto: Mapped[str] = mapped_column(Text, default="")
    questoes_resolvidas: Mapped[int] = mapped_column(Integer, default=0)
    questoes_corretas: Mapped[int] = mapped_column(Integer, default=0)

    def duracao_minutos(self):
        if self.data_inicio and self.data_fim:
            delta = self.data_fim - self.data_inicio
            return int(delta.total_seconds() // 60)
        return None

class Revisao(Base):
    __tablename__ = "revisoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais.id"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    assunto_id: Mapped[int] = mapped_column(ForeignKey("assuntos.id"))
    agendada_para: Mapped[dt.date] = mapped_column(Date)
    realizada: Mapped[bool] = mapped_column(Boolean, default=False)
    sessao_id: Mapped[int] = mapped_column(ForeignKey("sessoes.id"), nullable=True)

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(300))
    tipo: Mapped[str] = mapped_column(String(50))  # prova | prazo | meta | outro
    data_inicio: Mapped[dt.datetime] = mapped_column(DateTime)
    data_fim: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    descricao: Mapped[str] = mapped_column(Text, default="")

class Deck(Base):
    __tablename__ = "decks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    assunto_id: Mapped[int] = mapped_column(ForeignKey("assuntos.id"))
    dificuldade_base: Mapped[str] = mapped_column(String(20), default="Médio")  # Fácil|Médio|Difícil

class Flashcard(Base):
    __tablename__ = "flashcards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"))
    frente: Mapped[str] = mapped_column(Text)
    verso: Mapped[str] = mapped_column(Text)
    dificuldade: Mapped[str] = mapped_column(String(20), default="Médio")
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    due_date: Mapped[dt.date] = mapped_column(Date, default=dt.date.today)

class FlashcardReviewLog(Base):
    __tablename__ = "flashcard_reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("flashcards.id"))
    timestamp: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.now)
    quality: Mapped[int] = mapped_column(Integer)  # 0..5

class PracticeLog(Base):
    __tablename__ = "practice_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[dt.date] = mapped_column(Date, default=dt.date.today)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    assunto_id: Mapped[int] = mapped_column(ForeignKey("assuntos.id"))
    questoes_resolvidas: Mapped[int] = mapped_column(Integer, default=0)
    questoes_corretas: Mapped[int] = mapped_column(Integer, default=0)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

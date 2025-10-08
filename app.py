import os
import datetime as dt
import pandas as pd
import streamlit as st

from db import init_db, get_session, Disciplina, Assunto, Sessao, Revisao, Material, Evento
from utils import human_duration, today, start_of_week, end_of_week, ensure_dirs

st.set_page_config(page_title="Concurso Planner", page_icon="🎯", layout="wide")

ensure_dirs()
init_db()

st.title("🎯 Concurso Planner")
st.caption("Planejamento de estudos para concursos com sessões, revisões (repetição espaçada), flashcards e métricas.")

with st.sidebar:
    st.header("Ações rápidas")
    st.page_link("app.py", label="🏠 Início / Visão Geral", icon="🏠")
    st.page_link("pages/1_📊_Dashboard.py", label="📊 Dashboard", icon="📊")
    st.page_link("pages/2_📚_Sessões_e_Materiais.py", label="📚 Sessões & Materiais", icon="📚")
    st.page_link("pages/3_🧠_Flashcards.py", label="🧠 Flashcards", icon="🧠")
    st.page_link("pages/4_📅_Calendário_e_Eventos.py", label="📅 Calendário & Eventos", icon="📅")
    st.page_link("pages/5_✅_Questões_e_Métricas.py", label="✅ Questões & Métricas", icon="✅")
    st.page_link("pages/6_⚙️_Configurações.py", label="⚙️ Configurações", icon="⚙️")

st.markdown("""
Este app foi pensado para **concursos públicos** e reúne em um só lugar:
- **Sessões** de Estudo/Revisão com **relato final** (técnica de *recall* / ensinar a si mesmo).
- **Repetição espaçada** para materiais e para **flashcards**.
- **Calendário** de provas/prazos/metas.
- **Painel (dashboard)** com produtividade e evolução.
""")

# Resumo rápido da semana
sess = get_session()
hoje = today()
ini_sem = start_of_week(hoje)
fim_sem = end_of_week(hoje)

total_min = sess.query(Sessao).filter(Sessao.data_inicio >= ini_sem, Sessao.data_inicio <= fim_sem, Sessao.data_fim.isnot(None)).all()
minutos = sum([s.duracao_minutos() or 0 for s in total_min])

pendentes = sess.query(Revisao).filter(Revisao.agendada_para <= fim_sem, Revisao.realizada == False).count()
sessoes_realizadas = sess.query(Sessao).filter(Sessao.data_fim.isnot(None), Sessao.data_inicio >= ini_sem, Sessao.data_inicio <= fim_sem).count()

col1, col2, col3 = st.columns(3)
col1.metric("Tempo estudado (semana)", human_duration(minutos))
col2.metric("Revisões pendentes (até dom.)", pendentes)
col3.metric("Sessões finalizadas (semana)", sessoes_realizadas)

st.info("Use o menu lateral para navegar. Recomendo começar por **📚 Sessões & Materiais** e **⚙️ Configurações**.")

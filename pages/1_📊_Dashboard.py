import datetime as dt
import pandas as pd
import streamlit as st
import altair as alt

from db import get_session, Sessao, Revisao, PracticeLog, Assunto, Disciplina
from utils import today, start_of_week, end_of_week, human_duration

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")

sess = get_session()
hoje = today()
ini_sem = start_of_week(hoje)
fim_sem = end_of_week(hoje)

# KPIs
sessoes_sem = sess.query(Sessao).filter(Sessao.data_inicio >= ini_sem, Sessao.data_inicio <= fim_sem, Sessao.data_fim.isnot(None)).all()
min_sem = sum([s.duracao_minutos() or 0 for s in sessoes_sem])
rev_pend = sess.query(Revisao).filter(Revisao.agendada_para <= hoje, Revisao.realizada == False).count()

col1, col2, col3 = st.columns(3)
col1.metric("Tempo estudado (semana)", human_duration(min_sem))
col2.metric("Sessões finalizadas (semana)", len(sessoes_sem))
col3.metric("Revisões pendentes (hoje ou atrasadas)", rev_pend)

st.divider()

# Evolução semanal (últimas 8 semanas)
oito_semanas_atras = hoje - dt.timedelta(weeks=8)
sessoes_ult = sess.query(Sessao).filter(Sessao.data_inicio >= oito_semanas_atras, Sessao.data_fim.isnot(None)).all()
df = pd.DataFrame([
    {"dia": s.data_inicio.date(), "minutos": s.duracao_minutos() or 0} for s in sessoes_ult
])
if not df.empty:
    df_agg = df.groupby("dia")["minutos"].sum().reset_index()
    chart = alt.Chart(df_agg).mark_line(point=True).encode(
        x="dia:T", y="minutos:Q", tooltip=["dia:T", "minutos:Q"]
    ).properties(title="Minutos estudados por dia (últimas 8 semanas)", height=300)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Ainda não há sessões registradas para exibir a evolução.")

st.divider()

# Taxa de acertos por assunto (média das entradas em PracticeLog)
logs = sess.query(PracticeLog).all()
if logs:
    rows = []
    for l in logs:
        assunto = sess.get(Assunto, l.assunto_id)
        disciplina = sess.get(Disciplina, l.disciplina_id)
        taxa = (l.questoes_corretas / l.questoes_resolvidas * 100) if l.questoes_resolvidas else 0
        rows.append({"Disciplina": disciplina.nome if disciplina else "-", "Assunto": assunto.nome if assunto else "-", "Taxa de acerto (%)": round(taxa, 1)})
    df_taxa = pd.DataFrame(rows)
    df_plot = df_taxa.groupby(["Disciplina", "Assunto"])["Taxa de acerto (%)"].mean().reset_index()
    bar = alt.Chart(df_plot).mark_bar().encode(
        x="Taxa de acerto (%):Q",
        y=alt.Y("Assunto:N", sort="-x"),
        color="Disciplina:N",
        tooltip=list(df_plot.columns)
    ).properties(title="Taxa média de acertos por assunto", height=400)
    st.altair_chart(bar, use_container_width=True)
else:
    st.info("Registre questões na página **✅ Questões & Métricas** para ver a taxa de acertos por assunto.")

import calendar
import datetime as dt
import pandas as pd
import altair as alt
import streamlit as st

from db import get_session, Evento, Sessao, Revisao, Disciplina, Assunto, Material
from utils import today

st.set_page_config(page_title="Calendário & Eventos", page_icon="📅", layout="wide")
st.title("📅 Calendário & Eventos")

sess = get_session()

tab1, tab2 = st.tabs(["🗓️ Eventos", "📈 Distribuição de Sessões/Revisões"])

with tab1:
    st.subheader("Adicionar/visualizar eventos")
    titulo = st.text_input("Título do evento")
    tipo = st.selectbox("Tipo", ["prova","prazo","meta","outro"])
    data_ini = st.date_input("Data de início", value=dt.date.today())
    hora_ini = st.time_input("Hora de início", value=dt.datetime.now().replace(second=0, microsecond=0).time())
    inicio = dt.datetime.combine(data_ini, hora_ini)

    data_fim = st.date_input("Data de fim (opcional)", value=dt.date.today(), key="ev_data_fim")
    hora_fim = st.time_input("Hora de fim (opcional)", value=dt.datetime.now().replace(second=0, microsecond=0).time(), key="ev_hora_fim")
    fim = dt.datetime.combine(data_fim, hora_fim)
    desc = st.text_area("Descrição (opcional)")
    if st.button("Salvar evento", type="primary"):
        e = Evento(titulo=titulo, tipo=tipo, data_inicio=inicio, data_fim=(fim if fim>inicio else None), descricao=desc)
        sess.add(e); sess.commit()
        st.success("Evento salvo!")

    st.write("Próximos eventos:")
    hoje = dt.datetime.now()
    eventos = sess.query(Evento).filter(Evento.data_inicio>=hoje - dt.timedelta(days=1)).order_by(Evento.data_inicio).all()
    rows = [{
        "Quando": e.data_inicio.strftime("%d/%m/%Y %H:%M"),
        "Título": e.titulo,
        "Tipo": e.tipo,
        "Descrição": e.descricao[:120] + ("..." if len(e.descricao)>120 else "")
    } for e in eventos]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

with tab2:
    st.subheader("Distribuição diária de estudo e revisões")
    data_ini = st.date_input("De", value=today().replace(day=1))
    data_fim = st.date_input("Até", value=today())

    sessoes = sess.query(Sessao).filter(Sessao.data_inicio >= dt.datetime.combine(data_ini, dt.time.min),
                                        Sessao.data_inicio <= dt.datetime.combine(data_fim, dt.time.max),
                                        Sessao.data_fim.isnot(None)).all()
    df_ses = pd.DataFrame([{"dia": s.data_inicio.date(), "minutos": s.duracao_minutos() or 0, "tipo": s.tipo} for s in sessoes])
    if not df_ses.empty:
        agg = df_ses.groupby(["dia","tipo"])["minutos"].sum().reset_index()
        chart = alt.Chart(agg).mark_bar().encode(
            x="dia:T", y="minutos:Q", color="tipo:N",
            tooltip=["dia:T","tipo:N","minutos:Q"]
        ).properties(title="Minutos por dia (Estudo x Revisão)", height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sem sessões no intervalo selecionado.")

    revs = sess.query(Revisao).filter(Revisao.agendada_para >= data_ini, Revisao.agendada_para <= data_fim).all()
    df_rev = pd.DataFrame([{"dia": r.agendada_para, "status": "Feita" if r.realizada else "Pendente"} for r in revs])
    if not df_rev.empty:
        agg_r = df_rev.groupby(["dia","status"]).size().reset_index(name="qtd")
        rev_chart = alt.Chart(agg_r).mark_bar().encode(
            x="dia:T", y="qtd:Q", color="status:N", tooltip=["dia:T","status:N","qtd:Q"]
        ).properties(title="Revisões agendadas por dia", height=250)
        st.altair_chart(rev_chart, use_container_width=True)

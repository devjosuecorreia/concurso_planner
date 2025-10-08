import datetime as dt
import streamlit as st
import pandas as pd


from db import get_session, Disciplina, Assunto, PracticeLog
from utils import today

st.set_page_config(page_title="Questões & Métricas", page_icon="✅", layout="wide")
st.title("✅ Questões & Métricas")

sess = get_session()
disciplinas = sess.query(Disciplina).order_by(Disciplina.nome).all()
assuntos = sess.query(Assunto).order_by(Assunto.nome).all()

def assunto_options(disciplina_id):
    return [a for a in assuntos if a.disciplina_id == disciplina_id]

tab1, tab2 = st.tabs(["➕ Registrar questões", "📈 Relatórios"])

with tab1:
    if not disciplinas:
        st.warning("Cadastre Disciplinas/Assuntos em ⚙️ Configurações.")
    else:
        data = st.date_input("Data", value=today())
        disc = st.selectbox("Disciplina", options=disciplinas, format_func=lambda d: d.nome)
        ass = st.selectbox("Assunto", options=assunto_options(disc.id), format_func=lambda a: a.nome)
        qr = st.number_input("Questões resolvidas", min_value=0, step=1)
        qc = st.number_input("Questões corretas", min_value=0, step=1, value=0, help="Informe quantas acertou das resolvidas.")
        if st.button("Gravar", type="primary"):
            pl = PracticeLog(data=data, disciplina_id=disc.id, assunto_id=ass.id, questoes_resolvidas=qr, questoes_corretas=qc)
            sess.add(pl); sess.commit()
            st.success("Registro salvo!")

with tab2:
    logs = sess.query(PracticeLog).order_by(PracticeLog.data.desc()).all()
    if logs:
        df = pd.DataFrame([{
            "Data": l.data, 
            "Disciplina": next((d.nome for d in disciplinas if d.id==l.disciplina_id), "-"),
            "Assunto": next((a.nome for a in assuntos if a.id==l.assunto_id), "-"),
            "Resolvidas": l.questoes_resolvidas,
            "Corretas": l.questoes_corretas,
            "Taxa (%)": round((l.questoes_corretas / l.questoes_resolvidas * 100) if l.questoes_resolvidas else 0, 1)
        } for l in logs])
        st.dataframe(df, use_container_width=True)
        agg = (
            df.groupby("Data")[["Resolvidas", "Corretas"]]
            .sum()
            .reset_index()
)
        st.line_chart(agg.set_index("Data")[["Resolvidas","Corretas"]])
    else:
        st.info("Sem registros de questões ainda.")

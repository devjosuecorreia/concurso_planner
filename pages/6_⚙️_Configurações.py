import streamlit as st
import pandas as pd

from db import get_session, Disciplina, Assunto

st.set_page_config(page_title="Configurações", page_icon="⚙️", layout="wide")
st.title("⚙️ Configurações")

sess = get_session()

tab1, tab2 = st.tabs(["📘 Disciplinas", "🏷️ Assuntos"])

with tab1:
    st.subheader("Cadastrar nova disciplina")
    nome = st.text_input("Nome da disciplina")
    if st.button("Adicionar disciplina", type="primary"):
        if not nome.strip():
            st.error("Informe um nome.")
        else:
            d = Disciplina(nome=nome.strip())
            sess.add(d); sess.commit()
            st.success("Disciplina adicionada!")

    discs = sess.query(Disciplina).order_by(Disciplina.nome).all()
    st.write("Disciplinas existentes:")
    st.dataframe(pd.DataFrame([{"ID": d.id, "Nome": d.nome} for d in discs]), use_container_width=True)

with tab2:
    st.subheader("Cadastrar novo assunto")
    disciplinas = sess.query(Disciplina).order_by(Disciplina.nome).all()
    if not disciplinas:
        st.warning("Cadastre uma disciplina antes.")
    else:
        disc = st.selectbox("Disciplina", options=disciplinas, format_func=lambda d: d.nome)
        nome_a = st.text_input("Nome do assunto")
        if st.button("Adicionar assunto", type="primary"):
            if not nome_a.strip():
                st.error("Informe um nome de assunto.")
            else:
                a = Assunto(nome=nome_a.strip(), disciplina_id=disc.id)
                sess.add(a); sess.commit()
                st.success("Assunto adicionado!")

        assuntos = sess.query(Assunto).order_by(Assunto.nome).all()
        rows = [{
            "ID": a.id, "Assunto": a.nome, "Disciplina": next((d.nome for d in disciplinas if d.id==a.disciplina_id), "-")
        } for a in assuntos]
        st.write("Assuntos existentes:")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

import os
import uuid
import datetime as dt
import streamlit as st
import pandas as pd

from db import get_session, Disciplina, Assunto, Material, Revisao, Sessao
from scheduler import schedule_dates
from utils import today

st.set_page_config(page_title="Sessões & Materiais", page_icon="📚", layout="wide")
st.title("📚 Sessões & Materiais")

sess = get_session()

# Helpers para selects
disciplinas = sess.query(Disciplina).order_by(Disciplina.nome).all()
assuntos = sess.query(Assunto).order_by(Assunto.nome).all()

def assunto_options(disciplina_id):
    return [a for a in assuntos if a.disciplina_id == disciplina_id]

tab1, tab2, tab3 = st.tabs(["➕ Cadastrar Material (e agendar revisões)", "▶️ Nova Sessão", "📋 Pendências de Revisão"])

with tab1:
    st.subheader("Adicionar Material")
    if not disciplinas:
        st.warning("Antes, cadastre **Disciplinas/Assuntos** em ⚙️ Configurações.")
    else:
        colA, colB = st.columns(2)
        with colA:
            disc = st.selectbox("Disciplina", options=disciplinas, format_func=lambda d: d.nome, key="mat_disc")
            ass_list = assunto_options(disc.id)
            ass = st.selectbox("Assunto", options=ass_list, format_func=lambda a: a.nome, key="mat_ass")
            titulo = st.text_input("Título do material")
            tipo = st.selectbox("Tipo", ["video","pdf","docx","audio","texto"])
            notas = st.text_area("Notas (opcional)")
        with colB:
            arquivo = st.file_uploader("Arquivo (vídeo/pdf/docx/áudio opcional)", type=["mp4","mkv","mov","pdf","docx","mp3","m4a","wav"], accept_multiple_files=False)
            n_rev = st.number_input("Quantas revisões deseja fazer?", min_value=0, max_value=20, value=5, step=1)
            data_base = st.date_input("Data base para começar as revisões", value=today())

        if st.button("Salvar material e agendar revisões", type="primary", use_container_width=True):
            if not titulo:
                st.error("Informe um título.")
            else:
                filepath = None
                if arquivo is not None:
                    ext = os.path.splitext(arquivo.name)[1]
                    uid = str(uuid.uuid4())[:8]
                    safe_name = f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uid}{ext}"
                    up_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
                    up_dir = os.path.abspath(up_dir)
                    os.makedirs(up_dir, exist_ok=True)
                    filepath = os.path.join(up_dir, safe_name)
                    with open(filepath, "wb") as f:
                        f.write(arquivo.getbuffer())

                m = Material(titulo=titulo, tipo=tipo, filepath=filepath, disciplina_id=disc.id, assunto_id=ass.id, notas=notas)
                sess.add(m)
                sess.commit()

                if n_rev > 0:
                    dates = schedule_dates(data_base, int(n_rev))
                    for d in dates:
                        r = Revisao(material_id=m.id, disciplina_id=disc.id, assunto_id=ass.id, agendada_para=d, realizada=False)
                        sess.add(r)
                    sess.commit()
                st.success("Material cadastrado e revisões agendadas!")

with tab2:
    st.subheader("Nova Sessão de Estudo ou Revisão")
    tipo = st.selectbox("Tipo de sessão", ["estudo","revisao"])
    disc = st.selectbox("Disciplina", options=disciplinas, format_func=lambda d: d.nome, key="ses_disc")
    ass_list = assunto_options(disc.id)
    ass = st.selectbox("Assunto", options=ass_list, format_func=lambda a: a.nome, key="ses_ass")
    materiais = sess.query(Material).filter(Material.disciplina_id==disc.id, Material.assunto_id==ass.id).order_by(Material.titulo).all()
    mat = st.selectbox("Material (opcional)", options=[None]+materiais, format_func=lambda m: m.titulo if m else "—")
    data_ini = st.date_input("Data de início", value=dt.date.today())
    hora_ini = st.time_input("Hora de início", value=dt.datetime.now().replace(second=0, microsecond=0).time())
    ini = dt.datetime.combine(data_ini, hora_ini)
    data_fim = st.date_input("Data de fim (preencha ao encerrar)", value=dt.date.today(), key="data_fim")
    hora_fim = st.time_input("Hora de fim (preencha ao encerrar)", value=dt.datetime.now().replace(second=0, microsecond=0).time(), key="hora_fim")
    fim = dt.datetime.combine(data_fim, hora_fim)
    relato = st.text_area("Relato detalhado do que foi aprendido (técnica de recall) — obrigatório ao finalizar.", height=150)
    q_res = st.number_input("Questões resolvidas (opcional)", min_value=0, step=1)
    q_cor = st.number_input("Questões corretas (opcional)", min_value=0, step=1)

    if st.button("Salvar sessão", type="primary", use_container_width=True):
        if fim <= ini:
            st.error("Fim deve ser após o início.")
        elif not relato.strip():
            st.error("O relato final é obrigatório — descreva o que aprendeu.")
        else:
            s = Sessao(tipo=tipo, disciplina_id=disc.id, assunto_id=ass.id, material_id=(mat.id if mat else None),
                       data_inicio=ini, data_fim=fim, relato_texto=relato, questoes_resolvidas=q_res, questoes_corretas=q_cor)
            sess.add(s)
            sess.commit()

            # Se for revisão vinculada a material e existir revisão prevista para a data, marque como realizada
            if tipo == "revisao" and mat:
                revs = sess.query(Revisao).filter(Revisao.material_id==mat.id, Revisao.agendada_para<=fim.date(), Revisao.realizada==False).order_by(Revisao.agendada_para).all()
                if revs:
                    revs[0].realizada = True
                    revs[0].sessao_id = s.id
                    sess.commit()
            st.success("Sessão salva!")

with tab3:
    st.subheader("Revisões pendentes")
    hoje = dt.date.today()
    revs = sess.query(Revisao).filter(Revisao.realizada==False).order_by(Revisao.agendada_para).all()
    if not revs:
        st.info("Nenhuma revisão pendente.")
    else:
        data = [{
            "Data": r.agendada_para,
            "Disciplina": sess.get(Disciplina, r.disciplina_id).nome,
            "Assunto": sess.get(Assunto, r.assunto_id).nome,
            "Material": sess.get(Material, r.material_id).titulo
        } for r in revs]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

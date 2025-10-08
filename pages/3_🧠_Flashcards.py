import datetime as dt
import streamlit as st
import pandas as pd

from db import get_session, Disciplina, Assunto, Deck, Flashcard, FlashcardReviewLog
from scheduler import sm2_update
from utils import today

st.set_page_config(page_title="Flashcards", page_icon="🧠", layout="wide")
st.title("🧠 Flashcards (SM-2)")

sess = get_session()
disciplinas = sess.query(Disciplina).order_by(Disciplina.nome).all()
assuntos = sess.query(Assunto).order_by(Assunto.nome).all()

def assunto_options(disciplina_id):
    return [a for a in assuntos if a.disciplina_id == disciplina_id]

tab1, tab2, tab3 = st.tabs(["📦 Baralhos", "✍️ Criar Flashcards", "📝 Revisar (Hoje)"])

with tab1:
    st.subheader("Gerenciar Baralhos")
    if not disciplinas:
        st.warning("Cadastre Disciplinas/Assuntos em ⚙️ Configurações.")
    else:
        disc = st.selectbox("Disciplina", options=disciplinas, format_func=lambda d: d.nome, key="deck_disc")
        ass = st.selectbox("Assunto", options=assunto_options(disc.id), format_func=lambda a: a.nome, key="deck_ass")
        nome = st.text_input("Nome do baralho")
        dif = st.selectbox("Dificuldade base", ["Fácil","Médio","Difícil"], index=1)
        if st.button("Criar baralho", type="primary"):
            d = Deck(nome=nome, disciplina_id=disc.id, assunto_id=ass.id, dificuldade_base=dif)
            sess.add(d); sess.commit()
            st.success("Baralho criado!")

        st.write("Baralhos existentes:")
        decks = sess.query(Deck).order_by(Deck.nome).all()
        data = [{
            "Nome": d.nome,
            "Disciplina": sess.get(Disciplina, d.disciplina_id).nome,
            "Assunto": sess.get(Assunto, d.assunto_id).nome,
            "Dificuldade base": d.dificuldade_base,
            "Cards": sess.query(Flashcard).filter(Flashcard.deck_id==d.id).count()
        } for d in decks]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

with tab2:
    st.subheader("Criar Flashcards")
    decks = sess.query(Deck).order_by(Deck.nome).all()
    if not decks:
        st.info("Crie um baralho antes.")
    else:
        deck = st.selectbox("Baralho", options=decks, format_func=lambda d: d.nome)
        frente = st.text_area("Frente (pergunta)")        
        verso = st.text_area("Verso (resposta)")
        dif = st.selectbox("Dificuldade", ["Fácil","Médio","Difícil"], index=1)
        if st.button("Adicionar card", type="primary"):
            c = Flashcard(deck_id=deck.id, frente=frente, verso=verso, dificuldade=dif, ease_factor=2.5, interval_days=0, repetitions=0, due_date=today())
            sess.add(c); sess.commit()
            st.success("Card adicionado!")

with tab3:
    st.subheader("Revisar cards de hoje")
    hoje = today()
    due_cards = sess.query(Flashcard).filter(Flashcard.due_date <= hoje).order_by(Flashcard.due_date).all()
    if not due_cards:
        st.success("Nenhum card vencido hoje. 👏")
    else:
        # Sessão simples: um card por vez
        card = due_cards[0]
        st.info(f"Baralho: {sess.get(Deck, card.deck_id).nome} • Vencido em: {card.due_date}")
        st.write("**Frente:**")
        st.markdown(card.frente)
        if st.button("Mostrar resposta"):
            st.write("**Resposta:**")
            st.markdown(card.verso)
            quality = st.slider("Avalie seu recall (0=errei totalmente ... 5=perfeito)", 0, 5, 3)
            if st.button("Gravar avaliação e agendar próxima"):
                ef, reps, interval = sm2_update(card.ease_factor, card.repetitions, card.interval_days, quality)
                card.ease_factor = ef
                card.repetitions = reps
                card.interval_days = interval
                card.due_date = hoje + dt.timedelta(days=interval)
                sess.add(FlashcardReviewLog(card_id=card.id, quality=quality))
                sess.commit()
                st.success(f"Próxima revisão deste card em {card.due_date} (intervalo {interval} dias). Recarregue a página para o próximo.")

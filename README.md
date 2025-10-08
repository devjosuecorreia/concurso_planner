# Concurso Planner — Planejador de Estudos para Concursos (Streamlit)

Um aplicativo **100% em Python** (Streamlit + SQLite) para organizar seus estudos para concursos: 
- Sessões de **Estudo** e **Revisão** com registro de tempo e relato final (técnica de _recall_).
- **Repetição espaçada**: ao cadastrar um material/conteúdo, você informa quantas revisões quer e o app distribui automaticamente os intervalos.
- **Flashcards** com baralhos por **Disciplina**, **Assunto** e **Dificuldade**, incluindo agendamento com algoritmo **SM-2** (Anki-like).
- **Arquivos**: aceita vídeos, PDFs, Word (DOCX) e áudios. Os arquivos são guardados e podem ser pré-visualizados.
- **Calendário/Agenda** de provas, prazos e metas, além da visualização da distribuição de sessões/revisões no tempo.
- **Métricas**: sessões realizadas, revisões pendentes, taxa de acerto por assunto, tempo estudado e evolução semanal.
- **Questões**: registre por dia e assunto quantas questões fez e quantas acertou.

## Como executar

1. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate  # Windows PowerShell
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o app:
   ```bash
   streamlit run app.py
   ```

O banco de dados SQLite (`studyplanner.db`) é criado automaticamente na primeira execução.

## Observações

- Extração de texto de PDFs/DOCX é opcional. Se `pdfplumber`/`python-docx` não estiverem instalados, o app ainda funciona (apenas não extrai prévias de texto).
- Os arquivos enviados são salvos na pasta `uploads/`. Você pode organizar subpastas por disciplina/assunto se desejar.
- O algoritmo de espaçamento padrão para **materiais** usa intervalos crescentes típicos ([1, 3, 7, 14, 30, 60, 120] dias). Para **flashcards**, o agendamento é adaptativo (algoritmo SM‑2).

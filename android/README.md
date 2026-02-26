# Concurso Planner Android (Jetpack Compose)

Este módulo traz uma base Android nativa para o app de estudos para concursos.

## Funcionalidades implementadas

- Cadastro de **Disciplinas** e **Assuntos**.
- Cadastro de **Materiais** com suporte aos tipos: vídeo, PDF, DOCX, áudio e texto/link.
- Criação de **Sessões de Estudo** e **Sessões de Revisão**.
- Registro obrigatório de **relato de aprendizado** no encerramento da sessão.
- Geração automática de revisões por **repetição espaçada** ao cadastrar conteúdo.
- Registro de **questões resolvidas/corretas** por assunto e por dia.
- Estrutura para **flashcards** com dificuldade e agendamento.
- **Dashboard** com tempo estudado, revisões pendentes e taxa de acerto.
- **Notificações diárias** de revisões pendentes via WorkManager.
- **Calendário de eventos** (provas, prazos e metas) no modelo de dados.

## Arquitetura

- **UI:** Jetpack Compose + Material 3.
- **Dados locais:** Room.
- **Execução assíncrona:** Coroutines + Flow.
- **Notificações recorrentes:** WorkManager.

## Próximos passos

1. Criar projeto Android Studio e copiar os arquivos deste diretório para o módulo `app`.
2. Adicionar navegação com `Navigation Compose` para telas completas.
3. Integrar upload/abertura de arquivo com SAF (`ACTION_OPEN_DOCUMENT`).
4. Opcional: sincronizar em nuvem (Firebase/Supabase).

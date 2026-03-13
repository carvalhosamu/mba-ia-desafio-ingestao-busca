# Desafio MBA Engenharia de Software com IA - Full Cycle

## Objetivo

Este projeto implementa uma solução de RAG (Retrieval-Augmented Generation) que:

- lê um arquivo PDF;
- gera embeddings do conteúdo;
- armazena os vetores em PostgreSQL com `pgvector`;
- responde perguntas somente com base no contexto recuperado.

## Status atual

O fluxo principal está implementado e funcional:

- `src/ingest.py`: ingestão e indexação do PDF no `pgvector`.
- `src/search.py`: recuperação semântica e geração de resposta com prompt restritivo.
- `src/chat.py`: interface de chat no terminal.

Também há módulos compartilhados para reduzir duplicação:

- `src/llm_providers.py`: seleção dos providers de embeddings/chat (`google` ou `openai`).
- `src/pgvector_store.py`: fábrica de conexão com `PGVector`.

## Estrutura

```text
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
└── src/
	├── chat.py
	├── ingest.py
	├── llm_providers.py
	├── pgvector_store.py
	└── search.py
```

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose

## Configuração do ambiente

### 1) Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source ./venv/bin/activate
```

### 2) Instale as dependências

```bash
pip install -r requirements.txt
```

### 3) Configure variáveis de ambiente

```bash
cp .env.example .env
```

Preencha o arquivo `.env`.

Variáveis comuns:

- `PROVIDER_LLM`: `google` ou `openai`
- `DATABASE_URL`: exemplo `postgresql+psycopg://postgres:postgres@localhost:5432/rag`
- `PG_VECTOR_COLLECTION_NAME`: nome da coleção de vetores (ex.: `documents`)
- `PDF_PATH`: caminho do PDF relativo ao projeto (ex.: `document.pdf`)

Para Google:

- `GOOGLE_API_KEY`
- `GOOGLE_CHAT_MODEL` (ex.: `gemini-1.5-flash`)
- `GOOGLE_EMBEDDING_MODEL` (ex.: `models/embedding-001`)

Para OpenAI:

- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL` (ex.: `gpt-4o-mini`)
- `OPENAI_EMBEDDING_MODEL` (ex.: `text-embedding-3-small`)

## Banco de dados (PostgreSQL + pgvector)

Suba os serviços:

```bash
docker compose up -d
```

Verifique se os containers estão ativos:

```bash
docker compose ps
```

Se quiser garantir manualmente a extensão `vector`:

```bash
docker compose exec -T postgres psql -U postgres -d rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Execução

### 1) Ingestão do PDF

```bash
python src/ingest.py
```

### 2) Chat interativo

```bash
python src/chat.py
```

Durante o chat, digite sua pergunta ou `sair` para encerrar.

## Observações

- O `search.py` é utilizado como módulo pelo `chat.py`.
- O prompt de resposta força o modelo a responder apenas com base no contexto recuperado.
- Se a resposta não estiver no contexto, o sistema retorna: `Não tenho informações necessárias para responder sua pergunta.`

# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de Ingestão e Busca Semântica com LangChain e PostgreSQL (pgVector).

## Descrição

Este projeto implementa um sistema RAG (Retrieval Augmented Generation) que permite:
- **Ingestão**: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector
- **Busca**: Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF

## Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework**: LangChain
- **Banco de dados**: PostgreSQL + pgVector
- **Containerização**: Docker & Docker Compose
- **CLI**: Rich (para interface melhorada)

## Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose
- API Key da OpenAI (ou Google Gemini)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
# ou usando uv:
uv pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas API keys:
```env
OPENAI_API_KEY=sua_chave_aqui
# ou
GEMINI_API_KEY=sua_chave_aqui
```

## Configuração

O projeto usa `pydantic-settings` para gerenciar configurações. As variáveis de ambiente seguem o padrão de prefixos:

- `OPENAI_API_KEY` - API Key da OpenAI
- `OPENAI_LLM_MODEL` - Modelo LLM (padrão: `gpt-5-nano`)
- `OPENAI_EMBEDDING_MODEL` - Modelo de embeddings (padrão: `text-embedding-3-small`)
- `DATABASE_URL` - URL de conexão do PostgreSQL (padrão: `postgresql://postgres:postgres@localhost:5432/rag`)
- `DATABASE_COLLECTION_NAME` - Nome da coleção (padrão: `document_collection`)
- `PDF_PATH` - Caminho do arquivo PDF (padrão: `./document.pdf`)
- `PDF_CHUNK_SIZE` - Tamanho dos chunks (padrão: `1000`)
- `PDF_CHUNK_OVERLAP` - Overlap dos chunks (padrão: `150`)
- `SEARCH_K` - Número de resultados na busca (padrão: `10`)

## Execução

### 1. Subir o banco de dados

```bash
docker compose up -d
```

Isso iniciará um container PostgreSQL com a extensão pgVector na porta 5432.

### 2. Executar ingestão do PDF

Coloque o arquivo PDF na raiz do projeto com o nome `document.pdf` (ou configure o caminho no `.env`):

```bash
python src/ingest.py
```

O script irá:
- Carregar o PDF
- Dividir em chunks de 1000 caracteres com overlap de 150
- Criar embeddings para cada chunk
- Salvar no banco de dados PostgreSQL com pgVector

### 3. Rodar o chat

```bash
python src/chat.py
```

O sistema abrirá uma interface CLI onde você pode fazer perguntas sobre o conteúdo do PDF.

**Exemplo de uso:**
```
💬 Pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
✅ Resposta: O faturamento foi de 10 milhões de reais.
```

Para perguntas fora do contexto:
```
💬 Pergunta: Quantos clientes temos em 2024?
✅ Resposta: Não tenho informações necessárias para responder sua pergunta.
```

Para sair, digite: `sair`, `exit` ou `quit`

## Estrutura do Projeto

```
├── docker-compose.yml          # Configuração do PostgreSQL com pgVector
├── requirements.txt            # Dependências Python
├── pyproject.toml             # Configuração do projeto (uv)
├── .env.example               # Template de variáveis de ambiente
├── document.pdf               # PDF para ingestão
├── README.md                  # Este arquivo
├── CHALLENGE.md               # Especificação do desafio
└── src/
    ├── config.py              # Configurações centralizadas (pydantic-settings)
    ├── prompts.py             # Templates de prompts
    ├── ingest.py              # Script de ingestão do PDF
    ├── search.py              # Função de busca semântica
    ├── chat.py                # CLI para interação com usuário
    └── services/
        ├── __init__.py
        ├── embeddings.py       # Gerenciamento de embeddings
        ├── llm.py             # Gerenciamento de LLM
        └── vector_store.py     # Acesso ao banco vetorial
```

## Funcionalidades Implementadas

✅ Ingestão de PDF com chunks de 1000 caracteres e overlap de 150  
✅ Armazenamento de vetores no PostgreSQL com pgVector  
✅ Busca semântica com k=10 resultados mais relevantes  
✅ CLI interativo com Rich para melhor UX  
✅ Configuração centralizada com pydantic-settings  
✅ Suporte para OpenAI e Gemini  
✅ Tratamento de perguntas fora do contexto  
✅ Validações e tratamento de erros  

## Solução de Problemas

### Erro: "No module named 'src'"
Certifique-se de estar executando os scripts a partir da raiz do projeto.

### Erro: "The api_key client option must be set"
Verifique se a variável `OPENAI_API_KEY` está configurada no arquivo `.env` ou como variável de ambiente.

### Erro: "Arquivo PDF não encontrado"
Verifique se o arquivo `document.pdf` existe na raiz do projeto ou configure o caminho correto no `.env`.

### Erro de conexão com o banco
Certifique-se de que o Docker Compose está rodando:
```bash
docker compose ps
```

## Desenvolvimento

O projeto foi desenvolvido seguindo boas práticas:
- Separação de responsabilidades
- Configuração centralizada
- Código modular e reutilizável
- Tratamento de erros robusto
- Interface CLI intuitiva

## Licença

Este projeto foi desenvolvido como parte do desafio do MBA Engenharia de Software com IA - Full Cycle.

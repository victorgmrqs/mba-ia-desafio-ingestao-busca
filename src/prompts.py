"""Templates de prompts para o sistema RAG."""

RAG_PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def format_rag_prompt(contexto: str, pergunta: str) -> str:
    """
    Formata o prompt RAG com contexto e pergunta.
    
    Args:
        contexto: Contexto extraído do banco de dados vetorial
        pergunta: Pergunta do usuário
        
    Returns:
        Prompt formatado pronto para ser enviado ao LLM
    """
    return RAG_PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)

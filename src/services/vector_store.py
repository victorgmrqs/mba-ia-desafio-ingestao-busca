"""Serviço para gerenciar acesso ao banco vetorial (PGVector)."""

import sys
from pathlib import Path
from typing import List, Tuple

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from langchain_core.documents import Document
from langchain_postgres import PGVector

from src.config import Settings
from src.services.embeddings import get_embeddings


def get_vector_store(settings: Settings) -> PGVector:
    """
    Cria e retorna instância do PGVector configurada.
    
    Args:
        settings: Configurações da aplicação
        
    Returns:
        Instância do PGVector configurada
    """
    embeddings = get_embeddings(settings)
    
    return PGVector(
        embeddings=embeddings,
        collection_name=settings.database.collection_name,
        connection=settings.database.url,
        use_jsonb=settings.database.use_jsonb,
    )


def search_documents(
    question: str, 
    settings: Settings, 
    k: int = 10
) -> List[Tuple[Document, float]]:
    """
    Busca documentos similares no banco vetorial.
    
    Args:
        question: Pergunta do usuário para buscar documentos similares
        settings: Configurações da aplicação
        k: Número de resultados a retornar (padrão: 10)
        
    Returns:
        Lista de tuplas (Document, score) com os documentos mais similares
    """
    if not question or not question.strip():
        return []
    
    store = get_vector_store(settings)
    results = store.similarity_search_with_score(question, k=k)
    
    return results

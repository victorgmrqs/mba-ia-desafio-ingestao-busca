"""Função de busca semântica no banco vetorial."""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.config import get_settings
from src.services.vector_store import search_documents


def search_documents_for_question(question: str) -> str:
    """
    Busca documentos no banco vetorial e retorna contexto formatado.
    
    Args:
        question: Pergunta do usuário
        
    Returns:
        String formatada com o contexto dos documentos encontrados
    """
    if not question or not question.strip():
        return ""
    
    settings = get_settings()
    results = search_documents(question, settings, k=settings.search.k)
    
    if not results:
        return ""
    
    context_parts = []
    for document, score in results:
        context_parts.append(
            f'Documento (score: {score:.2f}):\n{document.page_content.strip()}\n'
        )
    
    return '\n---\n'.join(context_parts)

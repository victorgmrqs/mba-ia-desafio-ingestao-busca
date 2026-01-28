"""Serviço para gerenciar instâncias de embeddings."""

import os
import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import Settings, LLMProvider


def get_embeddings(settings: Settings):
    """
    Retorna instância de embeddings baseado no provedor configurado.
    
    Args:
        settings: Configurações da aplicação
        
    Returns:
        Instância de embeddings (OpenAIEmbeddings ou GoogleGenerativeAIEmbeddings)
    """
    if settings.llm_provider == LLMProvider.OPENAI:
        kwargs = {"model": settings.openai.embedding_model}
        # Tentar obter API key das configurações ou da variável de ambiente
        api_key = settings.openai.api_key or os.getenv("OPENAI_API_KEY")
        if api_key:
            kwargs["api_key"] = api_key
        return OpenAIEmbeddings(**kwargs)
    else:
        kwargs = {"model": settings.gemini.embedding_model}
        # Tentar obter API key das configurações ou da variável de ambiente
        api_key = settings.gemini.api_key or os.getenv("GEMINI_API_KEY")
        if api_key:
            kwargs["google_api_key"] = api_key
        return GoogleGenerativeAIEmbeddings(**kwargs)

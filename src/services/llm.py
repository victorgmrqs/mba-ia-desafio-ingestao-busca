"""Serviço para gerenciar instâncias de LLM."""

import os
import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Settings, LLMProvider


def get_llm(settings: Settings) -> BaseChatModel:
    """
    Retorna instância do LLM configurado baseado no provedor.
    
    Args:
        settings: Configurações da aplicação
        
    Returns:
        Instância do LLM (ChatOpenAI ou ChatGoogleGenerativeAI)
    """
    if settings.llm_provider == LLMProvider.OPENAI:
        kwargs = {
            "model": settings.openai.llm_model,
            "temperature": settings.openai.temperature,
        }
        # Tentar obter API key das configurações ou da variável de ambiente
        api_key = settings.openai.api_key or os.getenv("OPENAI_API_KEY")
        if api_key:
            kwargs["api_key"] = api_key
        if settings.openai.max_tokens:
            kwargs["max_tokens"] = settings.openai.max_tokens
        return ChatOpenAI(**kwargs)
    else:
        kwargs = {
            "model": settings.gemini.llm_model,
            "temperature": settings.gemini.temperature,
        }
        # Tentar obter API key das configurações ou da variável de ambiente
        api_key = settings.gemini.api_key or os.getenv("GEMINI_API_KEY")
        if api_key:
            kwargs["google_api_key"] = api_key
        return ChatGoogleGenerativeAI(**kwargs)

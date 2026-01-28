from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field, field_validator

# Caminho do arquivo .env relativo à raiz do projeto
ENV_FILE = Path(__file__).parent.parent / ".env"


class Environment(str, Enum):
    """Environments available for the application"""
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'


class LLMProvider(str, Enum):
    """LLM providers available"""
    OPENAI = 'openai'
    GEMINI = 'gemini'

class DatabaseConfig(BaseSettings):
    url: str = Field(
        default='postgresql://postgres:postgres@localhost:5432/rag',
        description='Connection string for the database'
    )
    collection_name: str = Field(
        default='document_collection',
        description='Name of the collection to vectorize the documents'
    )

    use_jsonb: bool = Field(
        default=True,
        description='Use JSONB fo the metadata'
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='DATABASE_',
        case_sensitive=False,
        extra="ignore",
    )

class PDFConfig(BaseSettings):
    path: str = Field(
        default='./document.pdf',
        description='Path to the PDF file'
    )
    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=2000,
        description='Chunk size for the PDF'
    )
    chunk_overlap: int = Field(
        default=150,
        ge=0,
        le=200,
        description='Chunk overlap for the PDF'
    )

    @field_validator('chunk_overlap')
    @classmethod
    def validate_overlap(cls, v:int, info) -> int:
        """Validate the chu
        nk overlap is less than the chunk_size"""
        if hasattr(info.data, 'chunk_size') and v >=info.data.get('chunk_size', 0):
            raise ValueError('chunk_overlap must be less than chunk_size')
        return v
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=False,
        extra="ignore",
    )

class OpenAIConfig(BaseSettings):
    api_key: Optional[str] = Field(
        default=None,
        description='API key for the OpenAI API'
    )
    embedding_model: Optional[str] = Field(
        default='text-embedding-3-small',
        description='Embedding model for the OpenAI API'
    )

    llm_model: Optional[str] = Field(
        default='gpt-5-nano',
        description='LLM model for the OpenAI API'
    )
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description='Temperature for the OpenAI API'
    )
    max_tokens:Optional[int] = Field(
        default=None,
        ge=1,
        description='Max tokens for the OpenAI API'
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='OPENAI_',
        case_sensitive=False,
        extra="ignore",
    )


class GeminiConfig(BaseSettings):
    """Configurações do Google Gemini."""
    
    api_key: Optional[str] = Field(
        default=None,
        description="API Key do Google Gemini"
    )
    embedding_model: str = Field(
        default="models/embedding-001",
        description="Modelo de embeddings do Gemini"
    )
    llm_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Modelo LLM do Gemini para respostas"
    )
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperatura para geração de texto"
    )
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="GEMINI_",
        case_sensitive=False,
        extra="ignore",
    )

class SearchConfig(BaseSettings):
    """Configurações de busca semântica."""
    
    k: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Número de resultados mais relevantes na busca"
    )
    score_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Threshold mínimo de similaridade (0-1)"
    )
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="SEARCH_",
        case_sensitive=False,
        extra="ignore",
    )


class Settings(BaseSettings):
    """Configuração principal da aplicação."""
    
    # Ambiente
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Ambiente de execução (dev, homol, prod)"
    )
    
    # Provedor de LLM padrão
    llm_provider: LLMProvider = Field(
        default=LLMProvider.OPENAI,
        description="Provedor de LLM padrão"
    )
    
    # Sub-configurações
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    pdf: PDFConfig = Field(default_factory=PDFConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
    
    # Configurações específicas por ambiente
    log_level: str = Field(
        default="INFO",
        description="Nível de log"
    )
    debug: bool = Field(
        default=False,
        description="Modo debug"
    )
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",  # Permite DATABASE_URL, OPENAI_API_KEY, etc.
    )
    
    @computed_field()
    @property
    def is_production(self) -> bool:
        """Verifica se está em produção."""
        return self.environment == Environment.PRODUCTION
    
    @computed_field
    @property
    def is_development(self) -> bool:
        """Verifica se está em desenvolvimento."""
        return self.environment == Environment.DEVELOPMENT
    
    @computed_field
    @property
    def is_homologation(self) -> bool:
        """Verifica se está em homologação."""
        return self.environment == Environment.HOMOLOGATION
    
    @field_validator("environment", mode="before")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Valida e normaliza o ambiente."""
        if isinstance(v, str):
            v = v.lower().strip()
            valid_envs = [e.value for e in Environment]
            if v not in valid_envs:
                raise ValueError(f"Ambiente deve ser um de: {', '.join(valid_envs)}")
        return v
    
    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Valida o nível de log."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if isinstance(v, str) and v.upper() not in valid_levels:
            raise ValueError(f"Log level deve ser um de: {', '.join(valid_levels)}")
        return v.upper() if isinstance(v, str) else v
    
    def get_embedding_model(self) -> str:
        """Retorna o modelo de embedding baseado no provedor selecionado."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self.openai.embedding_model
        return self.gemini.embedding_model
    
    def get_llm_model(self) -> str:
        """Retorna o modelo LLM baseado no provedor selecionado."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self.openai.llm_model
        return self.gemini.llm_model
    
    def get_api_key(self) -> Optional[str]:
        """Retorna a API key baseada no provedor selecionado."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self.openai.api_key
        return self.gemini.api_key


@lru_cache()
def get_settings() -> Settings:
    """
    Factory function para obter a instância de Settings.
    Usa lru_cache para garantir singleton.
    """
    return Settings()
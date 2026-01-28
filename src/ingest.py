"""Script de ingestão de PDF no banco vetorial."""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_settings
from src.services.vector_store import get_vector_store


def ingest_pdf():
    """
    Ingesta PDF no banco vetorial.
    
    Carrega o PDF, divide em chunks, cria embeddings e salva no banco.
    """
    settings = get_settings()
    
    # Validar se o arquivo PDF existe
    pdf_path = Path(settings.pdf.path)
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Arquivo PDF não encontrado: {pdf_path}. "
            f"Verifique a configuração PDF_PATH ou coloque o arquivo no caminho especificado."
        )
    
    print(f"Ingerindo PDF de: {pdf_path}")
    
    # Carregar PDF
    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()
    
    if not docs:
        raise ValueError("Nenhum documento foi carregado do PDF.")
    
    # Dividir em chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.pdf.chunk_size,
        chunk_overlap=settings.pdf.chunk_overlap
    )
    splits = splitter.split_documents(docs)
    
    if not splits:
        raise ValueError("Nenhum chunk foi criado do PDF.")
    
    # Enriquecer documentos (remover metadados vazios)
    enriched = [
        Document(
            page_content=document.page_content,
            metadata={
                key: value 
                for key, value in document.metadata.items() 
                if value not in ('', None)
            }
        )
        for document in splits
    ]
    
    print(f'Total de chunks criados: {len(enriched)}')
    
    # Criar IDs para os documentos
    ids = [f'doc-{index}' for index in range(len(enriched))]
    
    # Obter instância do vector store
    store = get_vector_store(settings)
    
    # Adicionar documentos ao banco
    print("Salvando documentos no banco vetorial...")
    store.add_documents(documents=enriched, ids=ids)
    
    print("Ingestão concluída com sucesso!")


if __name__ == "__main__":
    ingest_pdf()

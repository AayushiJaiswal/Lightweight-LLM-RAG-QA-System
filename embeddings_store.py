"""
Embeddings and Vector Store Module
Using LangChain + FAISS + sentence-transformers
"""

from typing import List, Dict
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class RAGRetriever:
    """RAG retriever using LangChain and FAISS"""

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {embedding_model}")
        print("(First time download ~90MB, may take 1-2 minutes)")

        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore: FAISS | None = None
        print("✓ Embedding model loaded")

    def index_documents(self, chunks: List[Dict[str, str]]):
        """Build FAISS index from document chunks"""
        print("\nBuilding FAISS vector index...")
        print("(This may take 1-2 minutes for first time)")

        if not chunks:
            raise ValueError(
                "No chunks provided to index_documents(). "
                "Ensure that DocumentChunker.chunk_documents produced at least one chunk."
            )

        documents: List[Document] = [
            Document(
                page_content=chunk["text"],
                metadata={
                    "source": chunk.get("source", "Unknown"),
                    "chunk_id": chunk.get("chunk_id", ""),
                    **chunk.get("metadata", {}),
                },
            )
            for chunk in chunks
            if chunk.get("text", "").strip()
        ]

        if not documents:
            raise ValueError(
                "All provided chunks were empty after filtering. "
                "Check your ingestion and chunking pipeline."
            )

        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        print(f"✓ FAISS index built with {len(documents)} vectors")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant chunks for query"""
        if self.vectorstore is None:
            raise ValueError("Index not built. Call index_documents() first.")

        results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        formatted_results: List[Dict] = [
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                # Convert distance to a relevance-like score if desired
                "score": float(1.0 - score),
                "metadata": doc.metadata,
            }
            for doc, score in results
        ]
        return formatted_results

    def save(self, save_dir: str = "data/embeddings"):
        """Save FAISS index to disk"""
        if self.vectorstore is None:
            raise ValueError("No vector store to save. Build the index first.")

        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        self.vectorstore.save_local(str(save_path))
        print(f"✓ Vector store saved to {save_dir}")

    def load(self, load_dir: str = "data/embeddings"):
        """Load FAISS index from disk"""
        load_path = Path(load_dir)
        if not load_path.exists():
            raise FileNotFoundError(f"No index found at {load_dir}")

        self.vectorstore = FAISS.load_local(
            str(load_path),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        print(f"✓ Vector store loaded from {load_dir}")

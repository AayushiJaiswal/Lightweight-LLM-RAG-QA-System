"""
Configuration for ERP RAG System with Ollama
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

class Config:
    # Paths
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    FEEDBACK_FILE = DATA_DIR / "feedback" / "feedback.jsonl"
    
    # Document Processing
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    MIN_CHUNK_SIZE = 50
    SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt', '.html', '.md']
    
    # Embedding Model
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    EMBEDDING_BATCH_SIZE = 32
    
    # Vector Store
    VECTOR_STORE = "faiss"
    
    # Ollama Configuration
    LLM_PROVIDER = "ollama"
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    OLLAMA_TEMPERATURE = 0.1
    MAX_GENERATION_TOKENS = 1000
    
    # Retrieval Settings
    DEFAULT_TOP_K = 5
    MIN_SIMILARITY_SCORE = 0.3
    
    # UI Settings
    UI_PORT = 7860
    UI_SHARE = False
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        print("✓ Directories created")
    
    @classmethod
    def validate_ollama(cls):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"✓ Ollama is running at {cls.OLLAMA_BASE_URL}")
                return True
        except:
            pass
        print(f"⚠️  Ollama not responding at {cls.OLLAMA_BASE_URL}")
        print("   Start with: ollama serve")
        return False
    
    @classmethod
    def print_config(cls):
        """Print configuration"""
        print("\n" + "="*60)
        print("ERP RAG SYSTEM CONFIGURATION")
        print("="*60)
        print(f"\n📚 Tech Stack:")
        print(f"  • Embeddings: {cls.EMBEDDING_MODEL}")
        print(f"  • Vector Store: {cls.VECTOR_STORE.upper()}")
        print(f"  • LLM: Ollama ({cls.OLLAMA_MODEL})")
        print(f"  • Framework: LangChain")
        print(f"\n⚙️  Settings:")
        print(f"  • Chunk Size: {cls.CHUNK_SIZE} words")
        print(f"  • Top-K Retrieval: {cls.DEFAULT_TOP_K}")
        print(f"  • Data Directory: {cls.RAW_DATA_DIR}")
        print("="*60 + "\n")

if __name__ == "__main__":
    Config.create_directories()
    Config.print_config()
    Config.validate_ollama()

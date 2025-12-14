"""
Document Ingestion and Chunking Module
Supports PDF, DOCX, TXT formats
"""

import re
from typing import List, Dict
from pathlib import Path
import PyPDF2
import docx


class DocumentIngester:
    """Handles multi-format document ingestion"""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def ingest_all(self) -> List[Dict[str, str]]:
        """Ingest all supported documents from directory"""
        documents: List[Dict[str, str]] = []

        for file_path in self.data_dir.rglob("*"):
            if file_path.suffix.lower() in [".pdf", ".docx", ".txt"]:
                doc = self._process_file(file_path)
                if doc and doc["content"].strip():
                    documents.append(doc)
                    print(f"  ✓ Processed: {file_path.name}")

        print(f"\n✓ Total documents ingested: {len(documents)}")
        return documents

    def _process_file(self, file_path: Path) -> Dict[str, str] | None:
        """Process single file based on extension"""
        try:
            suffix = file_path.suffix.lower()

            if suffix == ".pdf":
                text = self._parse_pdf(file_path)
            elif suffix == ".docx":
                text = self._parse_docx(file_path)
            elif suffix == ".txt":
                text = self._parse_txt(file_path)
            else:
                return None

            cleaned = self._clean_text(text)
            if not cleaned:
                # Skip completely empty files
                print(f"  ⚠️  Skipping empty file: {file_path.name}")
                return None

            return {
                "source": str(file_path.name),
                "content": cleaned,
                "path": str(file_path),
            }
        except Exception as e:
            print(f"  ⚠️  Error processing {file_path.name}: {e}")
            return None

    def _parse_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text

    def _parse_docx(self, file_path: Path) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)

    def _parse_txt(self, file_path: Path) -> str:
        """Read plain text file"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove weird control characters but keep typical punctuation
        text = re.sub(r"[^\w\s.,!?;:()\-\'\"]", "", text)
        return text.strip()


class DocumentChunker:
    """Splits documents into chunks for embedding"""

    def __init__(self, chunk_size: int = 350, chunk_overlap: int = 60):
        # Guard against invalid configuration
        if chunk_size <= chunk_overlap:
            raise ValueError("chunk_size must be greater than chunk_overlap")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Split documents into overlapping chunks"""
        chunks: List[Dict[str, str]] = []

        for doc in documents:
            content = doc.get("content", "").strip()
            if not content:
                continue

            doc_chunks = self._chunk_text(content)

            for i, chunk_text in enumerate(doc_chunks):
                chunks.append(
                    {
                        "text": chunk_text,
                        "source": doc["source"],
                        "chunk_id": f"{doc['source']}_chunk_{i}",
                        "metadata": {
                            "source_file": doc["source"],
                            "chunk_index": i,
                            "total_chunks": len(doc_chunks),
                        },
                    }
                )

        print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
        if len(chunks) == 0:
            print("⚠️  No chunks were created. Check that your documents contain enough text.")

        return chunks

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks: List[str] = []

        if not words:
            return chunks

        step = self.chunk_size - self.chunk_overlap

        for i in range(0, len(words), step):
            chunk_words = words[i : i + self.chunk_size]
            # Allow smaller paragraphs so more chunks are created
            if len(chunk_words) >= 10:
                chunks.append(" ".join(chunk_words))

        return chunks

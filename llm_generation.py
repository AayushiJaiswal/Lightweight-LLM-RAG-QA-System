"""
LLM Generation Module with Ollama
Using LangChain for RAG pipeline orchestration
"""

from typing import Dict
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate


class RAGPipeline:
    """Complete RAG pipeline using LangChain + Ollama"""

    def __init__(
        self,
        retriever,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
    ):
        """
        Initialize RAG pipeline with Ollama

        Args:
            retriever: RAGRetriever instance
            base_url: Ollama server URL
            model: Ollama model name (llama3.2, mistral, phi3, etc.)
        """
        self.retriever = retriever

        print(f"Initializing Ollama: {model}")

        try:
            self.llm = Ollama(
                base_url=base_url,
                model=model,
                temperature=0.1,
            )
            # Test connection
            _ = self.llm.invoke("Hi")
            print(f"✓ Ollama connected: {model}")
        except Exception as e:
            print(f"\n❌ Ollama connection failed: {e}")
            print("1. Check Ollama is running: ollama serve")
            print(f"2. Check model is pulled: ollama pull {model}")
            print(f"3. Test manually: ollama run {model}")
            raise

        template = """You are an ERP system expert assistant. Answer the question using ONLY the context provided below.

CONTEXT FROM ERP DOCUMENTATION:
{context}

INSTRUCTIONS:
1. Answer directly and concisely
2. Cite sources using [Source 1], [Source 2] format after each claim
3. If information is missing, say "I don't have that information in the provided documents"
4. Use bullet points for procedural questions
5. Be specific and factual

USER QUESTION: {query}

ANSWER:"""

        self.prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=template,
        )

        print("✓ RAG pipeline ready")

    def answer_question(self, query: str, top_k: int = 5) -> Dict:
        """Generate answer for query using RAG"""
        print(f"\n🔍 Searching for: '{query}'")
        context_chunks = self.retriever.retrieve(query, top_k=top_k)

        if not context_chunks:
            return {
                "answer": "I couldn't find relevant information in the ERP documentation.",
                "sources": [],
                "confidence": 0.0,
                "query": query,
            }

        print(f"✓ Found {len(context_chunks)} relevant chunks")

        # Build context text with source labels
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            source_label = f"[Source {i}: {chunk['source']}]"
            context_text += f"\n{source_label}\n{chunk['text']}\n"

        print("🤖 Generating answer with Ollama...")

        try:
            # Format the prompt and call the LLM directly
            final_prompt = self.prompt.format(
                context=context_text,
                query=query,
            )
            answer = self.llm.invoke(final_prompt).strip()
        except Exception as e:
            print(f"⚠️  Generation error: {e}")
            answer = "Error generating answer. Please check Ollama is running."

        avg_score = sum(c["score"] for c in context_chunks) / len(context_chunks)

        result = {
            "answer": answer,
            "sources": context_chunks,
            "confidence": avg_score,
            "query": query,
        }

        print("✓ Answer generated")
        return result

    def format_response(self, result: Dict) -> str:
        """Format response with citations for display"""
        output = f"**Answer:**\n{result['answer']}\n\n"

        if result["sources"]:
            output += "**Sources:**\n"
            for i, source in enumerate(result["sources"], 1):
                output += f"{i}. {source['source']} (Relevance: {source['score']:.2%})\n"
                # Short preview of the chunk text
                preview = source["text"][:150].replace("\n", " ")
                output += f"   └─ {preview}...\n\n"

        output += f"**Confidence:** {result['confidence']:.2%}"
        return output

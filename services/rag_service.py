import os
from typing import List, Dict, Any
from langchain_community.embeddings import FakeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import numpy as np

class RAGService:
    def __init__(self):
        import os
        self.embeddings = FakeEmbeddings(size=1536)
        self.persist_directory = "chroma_db"
        self.vector_store = None
        self.bm25 = None
        self.documents = []

    def initialize_vector_store(self, chunks: List[Dict[str, Any]]):
        """Initialize ChromaDB with document chunks."""
        docs = [Document(page_content=c["content"], metadata=c["metadata"]) for c in chunks]
        self.documents = docs
        self.vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Initialize BM25 for keyword search
        tokenized_corpus = [doc.page_content.split() for doc in docs]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def hybrid_retrieve(self, query: str, k: int = 5) -> List[Document]:
        """Hybrid retrieval combining Vector search and BM25."""
        if not self.vector_store:
            return []
            
        # 1. Vector Search
        vector_results = self.vector_store.similarity_search(query, k=k)
        
        # 2. BM25 Search
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_n_indices = np.argsort(bm25_scores)[-k:][::-1]
        bm25_results = [self.documents[i] for i in top_n_indices if bm25_scores[i] > 0]
        
        # Combine and deduplicate
        combined = {doc.page_content: doc for doc in vector_results + bm25_results}
        return list(combined.values())[:k]

    async def add_documents(self, chunks: List[Dict[str, Any]]):
        """Add new documents to existing store."""
        new_docs = [Document(page_content=c["content"], metadata=c["metadata"]) for c in chunks]
        if self.vector_store:
            self.vector_store.add_documents(new_docs)
            self.documents.extend(new_docs)
            # Re-init BM25
            tokenized_corpus = [doc.page_content.split() for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized_corpus)
        else:
            self.initialize_vector_store(chunks)

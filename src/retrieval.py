import faiss
import numpy as np
from typing import List, Dict, Tuple
import torch
from transformers import AutoTokenizer, AutoModel
import pickle
import os
import logging

class RAGRetriever:
    def __init__(self, embedding_dimension: int = 1536, index_path: str = 'models/faiss_index'):
        self.embedding_dimension = embedding_dimension
        self.index_path = index_path
        self.index = None
        self.document_store = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize FAISS index
        self._initialize_index()
        
        # Load document store if exists
        self._load_document_store()

    def _initialize_index(self):
        """Initialize FAISS index."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dimension)

    def _load_document_store(self):
        """Load document store from disk."""
        store_path = f"{self.index_path}_store.pkl"
        if os.path.exists(store_path):
            with open(store_path, 'rb') as f:
                self.document_store = pickle.load(f)

    def save_index(self):
        """Save index and document store to disk."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        
        store_path = f"{self.index_path}_store.pkl"
        with open(store_path, 'wb') as f:
            pickle.dump(self.document_store, f)

    def add_documents(self, documents: List[Dict], embeddings: np.ndarray):
        """Add documents and their embeddings to the index."""
        try:
            # Add embeddings to FAISS index
            self.index.add(embeddings)
            
            # Store document metadata
            start_idx = len(self.document_store)
            for idx, doc in enumerate(documents):
                self.document_store[start_idx + idx] = doc
            
            # Save updated index and store
            self.save_index()
        except Exception as e:
            self.logger.error(f"Error adding documents to index: {e}")
            raise

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar documents using query embedding."""
        try:
            # Ensure query embedding is 2D
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Search index
            distances, indices = self.index.search(query_embedding, k)
            
            # Retrieve documents and create result list
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx in self.document_store:
                    results.append((self.document_store[idx], float(distance)))
            
            return results
        except Exception as e:
            self.logger.error(f"Error searching index: {e}")
            raise

    def get_document_by_id(self, doc_id: int) -> Dict:
        """Retrieve document by ID."""
        return self.document_store.get(doc_id)


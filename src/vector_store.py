import faiss
import numpy as np

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_index(index, query_embedding, k=12):
    distances, indices = index.search(query_embedding, k)
    return indices, distances
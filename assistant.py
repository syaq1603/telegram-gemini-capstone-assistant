import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
gemini_model = genai.GenerativeModel("gemini-pro")

# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory FAISS index (re-initialize on every run)
embedding_dim = 384
faiss_index = faiss.IndexFlatL2(embedding_dim)
documents = []

def add_document(text, metadata=None):
    """Add a document to FAISS and local store"""
    embedding = embedder.encode([text])[0]
    faiss_index.add(np.array([embedding]))
    documents.append((text, metadata))

def retrieve_similar(query, top_k=3):
    """Retrieve top-k similar document chunks"""
    query_vec = embedder.encode([query])[0]
    D, I = faiss_index.search(np.array([query_vec]), top_k)
    return [documents[i][0] for i in I[0]]

def ask_gemini(question, context=None):
    """Generate a response using Gemini"""
    prompt = f"{context}\n\nQuestion: {question}" if context else question
    response = gemini_model.generate_content(prompt)
    return response.text

def rag_ask(question):
    """RAG-style Q&A: retrieve + ask Gemini"""
    context = "\n\n".join(retrieve_similar(question))
    return ask_gemini(question, context)

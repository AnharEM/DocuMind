import requests
import json
import re
import random
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from vector_store import search_index

# Constants
OLLAMA_MODEL = "phi3"
CONFIDENCE_THRESHOLD = 0.30

@st.cache_resource
def load_embed_model():
    """Loads and caches the embedding model."""
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_ollama(prompt):
    """Hits the local Ollama API with standard configuration."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": 4096,
                    "num_predict": 512,
                    "temperature": 0.3
                }
            },
            timeout=120 # Increased timeout for large docs
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        return "Error: Could not connect to Ollama."
    except Exception as e:
        return f"Error: {e}"

def extract_json_from_response(response_text):
    """Robust JSON extractor for LLM responses."""
    try:
        # 1. Try finding JSON code block
        match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        
        # 2. Try finding raw JSON object
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
            
        return None
    except:
        return None

@st.cache_data
def detect_document_type(text_sample):
    """Auto-detects the document type from the first 4000 chars."""
    prompt = f"""
    Analyze the text below and classify it into EXACTLY ONE of these categories:
    [Research Paper, Pitchdeck, Financial Report, Technical Documentation, Book Chapter, Legal Contract, General Article].
    
    Return ONLY the category name. Do not explain.
    
    Text:
    {text_sample[:2000]}
    """
    detected_type = query_ollama(prompt)
    
    valid_types = ["Research Paper", "Pitchdeck", "Financial Report", "Technical Documentation", "Book Chapter", "Legal Contract", "General Article"]
    for t in valid_types:
        if t.lower() in detected_type.lower():
            return t
    return "General Document"

def get_detail_level(text):
    """Determines detail level based on word count."""
    doc_length = len(text.split())
    if doc_length < 1500:
        return "concise but complete"
    elif doc_length < 5000:
        return "clear and moderately detailed"
    else:
        return "comprehensive and well-structured"

def generate_smart_summary(doc_type, text):
    """Generates a structured summary based on doc type."""
    detail_level = get_detail_level(text)
    structures = {
        "Research Paper": "Structure: ## ABSTRACT, ## METHODOLOGY, ## KEY FINDINGS, ## IMPLICATIONS.",
        "Pitchdeck": "Structure: ## THE PROBLEM, ## THE SOLUTION, ## MARKET OPPORTUNITY, ## THE ASK.",
        "Legal Contract": "Structure: ## PARTIES, ## OBLIGATIONS, ## TERMINATION, ## LIABILITY.",
        "Technical Documentation": "Structure: ## OVERVIEW, ## ARCHITECTURE, ## API USAGE, ## REQUIREMENTS.",
        "Financial Report": "Structure: ## EXEC SUMMARY, ## REVENUE, ## RISKS, ## OUTLOOK."
    }
    
    structure_prompt = structures.get(doc_type, "Structure: ## OVERVIEW, ## KEY THEMES, ## DETAILED POINTS, ## CONCLUSION.")
    content_slice = text[:6000] # Increased context window slightly
    
    prompt = f"""
    You are an expert analyst.
    Task: Provide a {detail_level} summary.
    Document Type: {doc_type}
    {structure_prompt}
    
    CRITICAL: 
    1. DO NOT use emojis. 
    2. Use provided headers exactly.
    3. Keep tone strictly professional and objective.
    
    Content:
    {content_slice}
    
    Format: Use clean Markdown with headers (##).
    """
    return query_ollama(prompt)

def retrieve_context(query, k=2):
    """Retrieves context with confidence score."""
    if not st.session_state.get("indexed", False):
        return None, 0.0

    embed_model = load_embed_model()
    index = st.session_state.index
    chunks = st.session_state.chunks

    query_embedding = embed_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    indices, distances = search_index(index, query_embedding, k=k)
    
    # Simple confidence metric
    confidence = 1 / (1 + distances[0][0])
    context = "\n\n".join([chunks[i] for i in indices[0]])
    return context, confidence

def generate_quiz_question():
    """Generates a quiz question from a random chunk."""
    if not st.session_state.get("chunks"):
        return None
        
    chunk = random.choice(st.session_state.chunks)
    prompt = f"""
    Create a multiple choice question from the text.
    Return purely VALID JSON with these keys:
    - question (string)
    - options (list of 4 strings)
    - correct_index (integer 0-3)
    - explanation (string: short reason for answer)
    
    Text:
    {chunk[:2000]}
    """
    res = query_ollama(prompt)
    return extract_json_from_response(res)

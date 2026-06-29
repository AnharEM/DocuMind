import requests
import numpy as np
import random
from sentence_transformers import SentenceTransformer
from pdf_utils import extract_text_from_pdf
from chunking import chunk_text
from vector_store import create_faiss_index, search_index

print("🚀 DocuMind Starting...\n")

# =========================
# CONFIG
# =========================

PDF_PATH = "data/sample.pdf"
OLLAMA_MODEL = "phi3"
CONFIDENCE_THRESHOLD = 0.30

# =========================
# LOAD DOCUMENT
# =========================

document_text = extract_text_from_pdf(PDF_PATH)
chunks = chunk_text(document_text)

print("🧠 Loading embedding model...")
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("🧠 Creating embeddings...")
embeddings = embed_model.encode(chunks)
embeddings = np.array(embeddings).astype("float32")

print("📦 Building FAISS index...")
index = create_faiss_index(embeddings)

print(f"✅ Indexed {len(chunks)} chunks.\n")

# =========================
# OLLAMA HELPER
# =========================

def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

# =========================
# RETRIEVAL
# =========================

def retrieve_context(query, k=5):
    query_embedding = embed_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    indices, distances = search_index(index, query_embedding, k=k)
    confidence = 1 / (1 + distances[0][0])

    context = "\n\n".join([chunks[i] for i in indices[0]])
    return context, confidence

# =========================
# UNIVERSAL SUMMARY
# =========================

def generate_summary():
    doc_length = len(document_text.split())

    if doc_length < 1500:
        detail = "concise but complete"
    elif doc_length < 5000:
        detail = "clear and moderately detailed"
    else:
        detail = "comprehensive and well-structured"

    prompt = f"""
You are an expert summarizer.

Provide a {detail} summary of the following document.

Do not assume the document type.
Do not invent information.
Focus only on key ideas, themes, arguments, and important details.
Ignore formatting artifacts.

Document:
{document_text[:12000]}
"""

    return ask_ollama(prompt)

# =========================
# RAG Q&A
# =========================

def answer_question(question):
    context, confidence = retrieve_context(question)

    if confidence < CONFIDENCE_THRESHOLD:
        return "Not found in document.", confidence

    prompt = f"""
Answer using ONLY the provided context.
If answer is not clearly present, respond exactly:
Not found in document.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = ask_ollama(prompt)
    return answer, confidence

# =========================
# MCQ MODE
# =========================

def mcq_mode():
    print("\n🎯 MCQ Mode (type 'quit' to exit)\n")
    score = 0
    total = 0

    while True:

        random_chunk = random.choice(chunks)

        prompt = f"""
Create ONE multiple choice question strictly from the context below.

Rules:
- Question must be answerable ONLY from the context.
- Provide exactly 4 options.
- Only one correct answer.
- Keep it concise.

Format exactly:

Question: ...
A) ...
B) ...
C) ...
D) ...
Correct: A/B/C/D

Context:
{random_chunk}
"""

        output = ask_ollama(prompt)

        try:
            parts = output.split("Correct:")
            question_block = parts[0].strip()
            correct_answer = parts[1].strip().upper()
        except:
            continue

        print("\n" + "="*50)
        print(question_block)
        print("="*50)

        user = input("Your answer (A/B/C/D or quit): ").strip().upper()

        if user == "QUIT":
            print(f"\nFinal Score: {score}/{total}\n")
            break

        if user not in ["A", "B", "C", "D"]:
            print("Invalid option.\n")
            continue

        total += 1

        if user == correct_answer:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {correct_answer}\n")

# =========================
# MENU LOOP
# =========================

while True:

    print("\n1. Summarize document")
    print("2. Ask question")
    print("3. MCQ mode")
    print("4. Exit")

    choice = input("Choose: ").strip()

    if choice == "1":
        print("\n🧠 Generating summary...\n")
        summary = generate_summary()

        print("="*60)
        print("📄 DOCUMENT SUMMARY")
        print("="*60)
        print(summary)
        print("="*60)

    elif choice == "2":
        question = input("\nEnter question: ")
        answer, confidence = answer_question(question)

        print("\n" + "="*60)
        print(answer)
        print("="*60)
        print(f"Confidence: {confidence:.2f}")

    elif choice == "3":
        mcq_mode()

    elif choice == "4":
        print("\nExiting DocuMind.")
        break

    else:
        print("Invalid choice.")
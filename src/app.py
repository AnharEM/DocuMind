import streamlit as st
import tempfile
import time
import numpy as np
import random 

# Local Modules
from pdf_utils import extract_text_from_pdf
from chunking import chunk_text
from vector_store import create_faiss_index

# New Modules
import ui_components as ui
import llm_logic as llm

# ==============================
# CONFIG & STATE
# ==============================
st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide")

# Apply Custom Ultra-Premium CSS
ui.apply_custom_css()

# Initialize Session State
if "indexed" not in st.session_state:
    st.session_state.indexed = False
if "doc_type" not in st.session_state:
    st.session_state.doc_type = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "current_quiz_idx" not in st.session_state:
    st.session_state.current_quiz_idx = -1

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2rem; text-align: center;">
        <h1 style="font-size: 3rem; margin:0; line-height: 1; letter-spacing: -2px; animation: logoPulse 4s infinite ease-in-out;">DOCU<br>MIND.</h1>
        <div style="height: 2px; background: #FFF; margin: 0.5rem auto; animation: lineExpand 1s ease-out forwards;"></div>
        <p style="font-size: 0.8rem; opacity: 0.7; letter-spacing: 1px;">SEMANTIC INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # State control in sidebar
    if st.session_state.indexed:
        if st.button("✕ CLOSE DOCUMENT", use_container_width=True):
            st.session_state.indexed = False
            st.session_state.doc_type = None
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.quiz_history = []
            st.session_state.current_quiz_idx = -1
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.indexed:
        st.success(">> SYSTEM READY")
        st.markdown(f"**TYPE:** `{st.session_state.doc_type}`")
        st.markdown(f"**CHUNKS:** `{len(st.session_state.get('chunks', []))}`")
    
    st.markdown("---")
    st.markdown("#### :: CORE CONFIG")
    st.code(f"MODEL: {llm.OLLAMA_MODEL}\nCHUNK: SMART", language="text")
    
    if st.session_state.indexed:
        st.markdown("#### :: DOC TYPE")
        doc_type_options = ["Research Paper", "Pitchdeck", "Financial Report", "Technical Documentation", "Book Chapter", "Legal Contract", "General Article"]
        current_type = st.session_state.doc_type
        if current_type not in doc_type_options:
            doc_type_options.append(current_type)
            
        new_doc_type = st.selectbox(
            "Classified As:",
            options=doc_type_options,
            index=doc_type_options.index(current_type) if current_type in doc_type_options else 0
        )
        if new_doc_type != st.session_state.doc_type:
            st.session_state.doc_type = new_doc_type
            st.rerun()

# ==============================
# MAIN DASHBOARD / UPLOAD
# ==============================
if not st.session_state.indexed:
    st.markdown("""
    <div style="text-align:center; padding-top: 10vh;">
        <h1 style="font-size: 5rem; margin-bottom: 0.5rem; letter-spacing: -0.05em;">DocuMind AI</h1>
        <p style="font-size: 1.2rem; color: rgba(255,255,255,0.6); margin-bottom: 3rem;">
            Advanced Semantic Analysis & Intelligence for your Documents.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Move File Uploader Here
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("Drop a PDF here to begin", type=["pdf"], label_visibility="collapsed")
    
    # --- PROCESSING LOGIC ---
    if uploaded_file:
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### :: INITIALIZING AI CORE ::")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text(">> READING PDF STREAM...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name
            progress_bar.progress(20)
            
            status_text.text(">> EXTRACTING TEXT LAYERS...")
            text = extract_text_from_pdf(pdf_path)
            progress_bar.progress(40)
            
            status_text.text(">> DETECTING SEMANTICS...")
            doc_type = llm.detect_document_type(text[:4000])
            progress_bar.progress(60)
            
            status_text.text(">> BUILDING VECTOR INDEX...")
            # Optimized Chunking Here
            chunks = chunk_text(text)
            
            embed_model = llm.load_embed_model()
            embeddings = embed_model.encode(chunks)
            embeddings = np.array(embeddings).astype("float32")
            index = create_faiss_index(embeddings)
            progress_bar.progress(100)
            
            st.session_state.text = text
            st.session_state.chunks = chunks
            st.session_state.index = index
            st.session_state.indexed = True
            st.session_state.doc_type = doc_type
            
            time.sleep(0.5) 
        
        placeholder.empty()
        st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: ui.render_feature_card("// AUTO-CLASSIFICATION", "Instantly detects if your doc is a pitchdeck, contract, or research paper.")
    with c2: ui.render_feature_card("|| CONFIDENCE ENGINE", "RAG answers come with semantic confidence scores to prevent hallucinations.")
    with c3: ui.render_feature_card("[] ACTIVE RECALL", "Test your mastery with AI-generated continuous quizzes.")
# ==============================
# MAIN DASHBOARD
# ==============================

else:
    st.markdown(f"## :: INTELLIGENT DASHBOARD")
    st.markdown(f"<p style='color:var(--text-secondary);'>ANALYZED AS: <b style='color:var(--text-primary);'>{st.session_state.doc_type}</b></p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["[DATA] INSIGHT ENGINE", "[QUERY] DEEP QUERY", "[QUIZ] QUIZ MODE"])
    
    # --- TAB 1: INSIGHTS ---
    with tab1:
        ui.render_feature_card("// STRUCTURED SUMMARY GENERATOR", "Generates a tailored summary structure based on the auto-detected document type.")
        st.info(f"Detected: **{st.session_state.doc_type}**")
        
        if st.button("Generate Smart Summary", type="primary"):
             with st.spinner("Synthesizing insights..."):
                summary = llm.generate_smart_summary(st.session_state.doc_type, st.session_state.text)
                clean_summary = summary.replace("```markdown", "").replace("```", "")
                ui.render_result_card("Executive Summary", clean_summary)

    # --- TAB 2: QUERY ---
    with tab2:
        ui.render_feature_card(":: SEMANTIC Q&A", "Ask specific questions about the document content. The AI will strictly verify facts.")
        
        question = st.text_input("Deep search your document:", placeholder="How does the methodology handle noise?")
        
        if st.button("ANALYZE", type="primary") and question:
            with st.spinner("TRAVERSING VECTOR SPACE..."):
                context, confidence = llm.retrieve_context(question)
                
                if confidence < llm.CONFIDENCE_THRESHOLD:
                    st.error(f"[WARNING] LOW CONFIDENCE ({confidence:.2f})")
                    st.markdown("The AI could not find sufficient evidence in the document to answer this unequivocally.")
                    with st.expander("Show nearest context found"):
                        st.info(context)
                else:
                    prompt = f"""
                    Answer using ONLY the context. Concise (3-4 sentences).
                    Context: {context}
                    Question: {question}
                    """
                    answer = llm.query_ollama(prompt)
                    
                    st.success(f"**Confidence Score: {confidence:.2f}**")
                    ui.render_result_card("Answer", answer, f"Reference Context:<br>{context[:1000]}...")

    # --- TAB 3: QUIZ ---
    with tab3:
        st.markdown(f"""
        <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex-grow: 1;">
                <h3 style="margin: 0; border:none;">[QUIZ] CONTINUOUS QUIZ MODE</h3>
                <p style="color: var(--text-secondary); margin: 0;">TEST YOUR KNOWLEDGE.</p>
            </div>
            <div style="font-size:1.5rem; font-weight:bold; color:var(--text-primary); border: 2px solid var(--border-color); padding: 5px 15px; border-radius: 0px;">
                {st.session_state.score} / {st.session_state.total}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 1. START QUIZ
        if st.session_state.current_quiz_idx == -1:
             if st.button("START QUIZ SESSION", type="primary"):
                 with st.spinner("Generating first question..."):
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
                    res = llm.query_ollama(prompt)
                    json_data = llm.extract_json_from_response(res)
                    
                    if json_data:
                        st.session_state.quiz_history.append({
                            "data": json_data, "answered": False, "user_answer": None, "feedback": None
                        })
                        st.session_state.current_quiz_idx = 0
                        st.rerun()
                    else: st.warning("Failed to generate question. Please try again.")

        # 2. ACTIVE QUIZ
        else:
            current_idx = st.session_state.current_quiz_idx
            if current_idx < 0 or current_idx >= len(st.session_state.quiz_history):
                st.session_state.current_quiz_idx = -1
                st.rerun()
            
            current_q = st.session_state.quiz_history[current_idx]
            q_data = current_q["data"]
            
            st.markdown(f"### Q{current_idx + 1}: {q_data.get('question')}")
            
            # Sanitize Options
            options = q_data.get('options', [])
            safe_options = [str(opt) if not isinstance(opt, dict) else str(list(opt.values())[0]) for opt in options]
            while len(safe_options) < 4: safe_options.append(f"Option {len(safe_options)+1}")
            
            if not current_q["answered"]:
                user_choice_idx = st.radio("Select Answer:", range(len(safe_options)), format_func=lambda x: safe_options[x], key=f"q_{current_idx}")
                
                if st.button("Submit Answer", type="primary"):
                    current_q["answered"] = True
                    current_q["user_answer"] = user_choice_idx
                    st.session_state.total += 1
                    
                    if user_choice_idx == q_data.get('correct_index', 0):
                        st.session_state.score += 1
                        # st.balloons() # REMOVED FOR STRICT B&W
                        current_q["feedback"] = {"type": "success", "msg": "[CORRECT] ANSWER ACCEPTED", "expl": q_data.get('explanation', '')}
                    else:
                        current_q["feedback"] = {"type": "error", "msg": f"[WRONG] THE CORRECT ANSWER IS: **{safe_options[q_data.get('correct_index', 0)]}**", "expl": q_data.get('explanation', '')}
                    st.rerun()
            else:
                st.info(f"YOU SELECTED: **{safe_options[current_q['user_answer']]}**")
                fb = current_q["feedback"]
                if fb:
                    if fb["type"] == "success": st.success(fb["msg"])
                    else: st.error(fb["msg"])
                    st.markdown(f"**EXPLANATION:** {fb['expl']}")

            st.markdown("---")
            c1, c2, c3, c4 = st.columns([1, 1, 2, 1])
            
            with c1:
                if current_idx > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.current_quiz_idx -= 1
                        st.rerun()
            
            with c2:
                is_last = (current_idx == len(st.session_state.quiz_history) - 1)
                if is_last:
                    if current_q["answered"]:
                        if st.button("Next Question ➡️", type="primary"):
                             with st.spinner("Generating next..."):
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
                                res = llm.query_ollama(prompt)
                                json_data = llm.extract_json_from_response(res)
                                if json_data:
                                    st.session_state.quiz_history.append({
                                        "data": json_data, "answered": False, "user_answer": None, "feedback": None
                                    })
                                    st.session_state.current_quiz_idx += 1
                                    st.rerun()
                    else: st.button("Next Question ➡️", disabled=True)
                else:
                     if st.button("Next ➡️"):
                        st.session_state.current_quiz_idx += 1
                        st.rerun()

            with c4:
                if st.button("Quit Session"):
                    st.session_state.quiz_history = []
                    st.session_state.current_quiz_idx = -1
                    st.session_state.score = 0
                    st.session_state.total = 0
                    st.rerun()
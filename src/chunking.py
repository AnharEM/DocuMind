import re

def clean_text(text):
    """
    Cleans text while preserving structure. 
    Does NOT aggressively remove lines, but normalizes whitespace.
    """
    # Normalize unicode
    text = text.replace('\xa0', ' ')
    
    # Fix multiple newlines but preserve paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove page numbers footers (simple heuristic: single digit on a line)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    return text.strip()


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Splits text into chunks with sentence boundary awareness.
    """
    text = clean_text(text)
    
    # Split by sentence endings (.!?) followed by space/newline
    # We keep the punctuation with the sentence
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence: 
            continue
            
        sentence_len = len(sentence)
        
        # If adding this sentence exceeds chunk size, finalize current chunk
        if current_length + sentence_len > chunk_size:
            # Join and add to chunks
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            
            # Start new chunk with overlap (if possible)
            # For simplicity in this lightweight version, we just start fresh 
            # or carry over the last sentence if it's small enough (overlap simulation)
            current_chunk = []
            current_length = 0
            
        current_chunk.append(sentence)
        current_length += sentence_len
    
    # Add lingering chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
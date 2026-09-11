"""
OmegaLoop: Socratic Quantum Workspace - Local Development & RAG API Server
Provides static file serving, PDF parsing with pypdf, text chunking, and RAG similarity retrieval.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import io
import re
import math
from collections import Counter
try:
    import pypdf
except ImportError:
    pypdf = None

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
    "over", "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself"
}

def tokenize(text: str):
    words = re.findall(r'[a-zA-Z0-9_\-\\]+', text.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]

def chunk_text(text: str, filename: str, chunk_size: int = 600, overlap: int = 150):
    clean = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start = 0
    idx = 1
    total_len = len(clean)

    while start < total_len:
        end = min(start + chunk_size, total_len)
        chunk_str = clean[start:end]
        tokens = tokenize(chunk_str)
        tf = dict(Counter(tokens))
        
        chunks.append({
            "id": f"{filename}_chunk_{idx}",
            "docName": filename,
            "chunkIndex": idx,
            "text": chunk_str,
            "tf": tf
        })
        idx += 1
        if end >= total_len:
            break
        start += (chunk_size - overlap)

    return chunks

def cosine_similarity(tf1: dict, tf2: dict) -> float:
    common = set(tf1.keys()) & set(tf2.keys())
    if not common:
        return 0.0
    dot = sum(tf1[k] * tf2[k] for k in common)
    mag1 = math.sqrt(sum(v * v for v in tf1.values()))
    mag2 = math.sqrt(sum(v * v for v in tf2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

class OmegaLoopHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == "/api/upload":
            self.handle_upload()
        elif self.path == "/api/rag_query":
            self.handle_rag_query()
        elif self.path == "/api/generate_challenge":
            self.handle_challenge()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_upload(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            
            # Check if JSON payload with base64/raw text or multipart
            try:
                payload = json.loads(post_data.decode("utf-8"))
                filename = payload.get("filename", "document.txt")
                raw_text = payload.get("text", "")
                
                # If raw_text is empty, check for base64 file data
                if not raw_text and "base64" in payload:
                    import base64
                    file_bytes = base64.b64decode(payload["base64"])
                    if filename.lower().endswith(".pdf"):
                        if pypdf:
                            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                            pages_text = [p.extract_text() or "" for p in reader.pages]
                            raw_text = "\n".join(pages_text)
                        else:
                            raw_text = file_bytes.decode("utf-8", errors="replace")
                    else:
                        raw_text = file_bytes.decode("utf-8", errors="replace")
            except Exception:
                # Direct raw text body
                filename = "uploaded_document.txt"
                raw_text = post_data.decode("utf-8", errors="replace")

            chunks = chunk_text(raw_text, filename)

            response_data = {
                "success": True,
                "filename": filename,
                "totalLength": len(raw_text),
                "chunkCount": len(chunks),
                "chunks": chunks
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_rag_query(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            payload = json.loads(post_data.decode("utf-8"))

            query = payload.get("query", "")
            chunks = payload.get("chunks", [])
            threshold = float(payload.get("threshold", 0.15))
            top_k = int(payload.get("top_k", 3))

            query_tokens = tokenize(query)
            query_tf = dict(Counter(query_tokens))

            scored = []
            for ch in chunks:
                ch_tf = ch.get("tf", {})
                score = cosine_similarity(query_tf, ch_tf)
                if score >= threshold:
                    scored.append({
                        "id": ch.get("id"),
                        "docName": ch.get("docName"),
                        "chunkIndex": ch.get("chunkIndex"),
                        "text": ch.get("text"),
                        "score": round(score, 4)
                    })

            scored.sort(key=lambda x: x["score"], reverse=True)
            top_matches = scored[:top_k]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "matches": top_matches}).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_challenge(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            payload = json.loads(post_data.decode("utf-8"))

            topic = payload.get("topic", "1D Infinite Potential Well")
            difficulty = payload.get("difficulty", "basic").lower()
            if difficulty not in ["basic", "medium", "hard"]:
                difficulty = "basic"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "topic": topic,
                "difficulty": difficulty,
                "validated": True
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run_streamlit():
    """Streamlit Cloud & Web Entry Point for OmegaLoop."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(
        page_title="OmegaLoop: Socratic Quantum Workspace",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Clean styling to maximize viewport for OmegaLoop
    st.markdown("""
    <style>
        #MainMenu, footer, header, .stDeployButton {display: none !important;}
        div.block-container {
            padding: 0rem !important;
            margin: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100% !important;
            height: 98vh !important;
            min-height: 850px;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    html_path = os.path.join(DIRECTORY, "index.html")
    if not os.path.exists(html_path):
        # Search parent directories and current directory for index.html
        for cand in [
            os.path.join(os.getcwd(), "index.html"),
            os.path.join(os.getcwd(), "Python_chatbot", "index.html"),
            os.path.join(os.path.dirname(DIRECTORY), "index.html"),
            os.path.join(os.path.dirname(DIRECTORY), "Python_chatbot", "index.html")
        ]:
            if os.path.exists(cand):
                html_path = cand
                break

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=920, scrolling=True)
    else:
        st.error("index.html not found. Please ensure index.html exists in the repository.")

def main():
    global PORT
    httpd = None
    for p in range(PORT, PORT + 20):
        try:
            httpd = ReusableTCPServer(("", p), OmegaLoopHandler)
            PORT = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"Error: Could not bind server to ports {PORT}-{PORT+19}")
        return

    url = f"http://localhost:{PORT}/index.html"
    print("=" * 65)
    print(" Ω  OmegaLoop: Socratic Quantum Workspace (RAG & Multi-Tier)")
    print(" Active First-Principles Quantum Tutoring | UN SDG 4")
    print("=" * 65)
    print(f" -> Serving frontend & RAG endpoints at: {url}")
    print(" -> Endpoints: /api/upload, /api/rag_query, /api/generate_challenge")
    print(" Press Ctrl+C to terminate.")
    print("=" * 65)
    
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down OmegaLoop workspace server.")
    finally:
        httpd.server_close()

# Detect if running under Streamlit (e.g. `streamlit run server.py` on Streamlit Cloud)
_is_streamlit = False
try:
    import streamlit as _st
    if getattr(_st, "runtime", None) is not None and _st.runtime.exists():
        _is_streamlit = True
except Exception:
    _is_streamlit = False

if _is_streamlit:
    run_streamlit()
elif __name__ == "__main__":
    main()

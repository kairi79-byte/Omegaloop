# Streamlit Cloud Entry Point for OmegaLoop
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from server import run_streamlit

if __name__ == "__main__":
    run_streamlit()

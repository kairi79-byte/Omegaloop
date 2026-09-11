"""
OmegaLoop Prototype Launcher (trial1)
Opens trial1.html prototype in the default browser.
"""

import webbrowser
import os

def main():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "trial1.html"))
    if os.path.exists(file_path):
        print(f"Opening trial1 prototype: {file_path}")
        webbrowser.open(f"file://{file_path}")
    else:
        print("trial1.html not found.")

if __name__ == "__main__":
    main()
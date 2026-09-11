import os
import time
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. PAGE SETUP & MODERN DARK STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tau | Quantum Socratic Tutor",
    layout="wide",
    page_icon="⚛️",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern sci-fi dark aesthetics
st.markdown("""
<style>
    /* Global style adjustments */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #0d1321 0%, #050811 100%);
        color: #e0e6ed;
    }
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 12px 16px;
        border-radius: 10px;
        backdrop-filter: blur(8px);
    }
    /* Header title glow */
    .title-glow {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ADB5, #00FFF0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    /* Module banner card */
    .module-card {
        background: rgba(13, 27, 42, 0.7);
        border-left: 4px solid #00ADB5;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CURRICULUM DEFINITIONS (3 STRICT MODULES)
# ---------------------------------------------------------
MODULES = {
    "1. Particle in a 1D Box": {
        "title": "Particle in an Infinite Potential Well",
        "desc": "Find the normalized ground-state wavefunction ψ(x) for a particle trapped between x = 0 and x = L.",
        "placeholder": "e.g. sqrt(2/L)*sin(pi*x/L)",
        "target_type": "wavefunction_box"
    },
    "2. Quantum Harmonic Oscillator": {
        "title": "Quantum Harmonic Oscillator Ground Energy",
        "desc": "Derive the ground-state zero-point energy E₀ in terms of ħ and ω using ladder operators or the Schrödinger equation.",
        "placeholder": "e.g. (1/2)*hbar*omega",
        "target_type": "energy_sho"
    },
    "3. Spin-1/2 Systems": {
        "title": "Spin Superposition Normalization",
        "desc": "Given an equal superposition state |ψ⟩ = c(|↑⟩ + |↓⟩) where c is real and positive, find the normalization constant c.",
        "placeholder": "e.g. 1/sqrt(2)",
        "target_type": "spin_norm"
    }
}

# ---------------------------------------------------------
# 3. MATHEMATICAL VALIDATION & PLOTS
# ---------------------------------------------------------
def verify_answer(user_input: str, target_type: str) -> bool:
    try:
        if target_type == "wavefunction_box":
            x, L = sp.symbols('x L', positive=True, real=True)
            target = sp.sqrt(2/L) * sp.sin(sp.pi * x / L)
            user_expr = sp.sympify(user_input)
            return sp.simplify(user_expr - target) == 0
        elif target_type == "energy_sho":
            hbar, omega = sp.symbols('hbar omega', positive=True, real=True)
            target = sp.Rational(1, 2) * hbar * omega
            user_expr = sp.sympify(user_input)
            return sp.simplify(user_expr - target) == 0
        elif target_type == "spin_norm":
            target = 1 / sp.sqrt(2)
            user_expr = sp.sympify(user_input)
            return sp.simplify(user_expr - target) == 0
    except Exception:
        return False
    return False

def generate_module_plot(module_key: str, solved: bool):
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='#050811')
    ax.set_facecolor('#0d1321')
    ax.tick_params(colors='#8892b0', labelsize=8)
    for spine in ax.spines.values():
        spine.set_color('#1e293b')

    if "Box" in module_key:
        x = np.linspace(0, 1.0, 400)
        prob = (np.sqrt(2) * np.sin(np.pi * x))**2 if solved else np.zeros_like(x)
        ax.plot(x, prob, color='#00ADB5', lw=2)
        ax.fill_between(x, prob, color='#00ADB5', alpha=0.25)
        ax.set_xlim(0, 1.0)
        ax.set_ylim(0, 2.5)
        ax.set_title("Probability Density |ψ(x)|²", color='#e0e6ed', fontsize=10)
        ax.axvline(0, color='#ff0055', lw=2, linestyle="--")
        ax.axvline(1.0, color='#ff0055', lw=2, linestyle="--")
    elif "Harmonic" in module_key:
        x = np.linspace(-3, 3, 400)
        potential = 0.5 * x**2
        ax.plot(x, potential, color='#ffaa00', lw=2, label="V(x)=½mω²x²")
        if solved:
            ax.axhline(0.5, color='#00ADB5', lw=2, linestyle="--", label="E₀ = ½ħω")
        ax.set_ylim(0, 3)
        ax.set_title("Parabolic Potential Well", color='#e0e6ed', fontsize=10)
        ax.legend(facecolor='#0d1321', edgecolor='#1e293b', labelcolor='#e0e6ed', fontsize=8)
    else:  # Spin-1/2
        angles = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(angles), np.sin(angles), color='#3b82f6', lw=1.5, linestyle=":")
        if solved:
            ax.arrow(0, 0, 0.707, 0.707, head_width=0.08, head_length=0.08, fc='#00ADB5', ec='#00ADB5', lw=2)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title("Spin State Projection", color='#e0e6ed', fontsize=10)
        ax.axhline(0, color='#1e293b')
        ax.axvline(0, color='#1e293b')

    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. STATE INITIALIZATION & SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#00ADB5; margin-bottom:0;'>⚛️ Tau Control</h2>", unsafe_allow_html=True)
    st.caption("Active Socratic Tutor | SDG 4")
    st.divider()

    selected_module_key = st.selectbox("Select Active Module:", list(MODULES.keys()))
    current_module = MODULES[selected_module_key]

    # Reset state if the user switches module
    if "current_module" not in st.session_state or st.session_state.current_module != selected_module_key:
        st.session_state.current_module = selected_module_key
        st.session_state.messages = []
        st.session_state.start_time = time.time()
        st.session_state.hints_used = 0
        st.session_state.solved = False

        system_instruction = f"""
        You are Tau, a world-class theoretical physicist and Socratic tutor.
        Your student is working EXCLUSIVELY on this challenge:
        "{current_module['title']}: {current_module['desc']}"

        STRICT RULES:
        1. NEVER output the final derivation, equation, or numeric answer.
        2. STRICT BOUNDARY: If the user asks about ANY topic outside of "{current_module['title']}" (e.g. pop culture, other sciences, general code, or unrelated physics), refuse politely:
           "My focus is locked to {current_module['title']}. Let's stay centered on resolving this problem."
        3. Provide incremental Socratic questions to scaffold their reasoning (physical intuition -> boundary principles -> algebraic setup).
        4. Max 2-3 sentences per answer. End with a question.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.sidebar.text_input("Gemini API Key (optional):", type="password", key="user_api_key")
        
        if api_key:
            try:
                client = genai.Client(api_key=api_key)
                st.session_state.chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                    ),
                )
            except Exception as e:
                st.session_state.chat = None
                st.sidebar.warning(f"Could not initialize Gemini Client: {e}")
        else:
            st.session_state.chat = None
            st.sidebar.info("Running in offline Socratic mode. Enter a GEMINI_API_KEY to enable live Gemini streaming.")

    # Coherence score tracking
    elapsed = int(time.time() - st.session_state.start_time)
    decay = (elapsed // 15) * 2 + (st.session_state.hints_used * 5)
    coherence = max(10, 100 - decay) if not st.session_state.solved else st.session_state.get("final_score", 100)

    st.write("### System Diagnostics")
    m1, m2 = st.columns(2)
    m1.metric("Coherence", f"{coherence}%")
    m2.metric("Hints", st.session_state.hints_used)

    st.write("---")
    st.pyplot(generate_module_plot(selected_module_key, st.session_state.solved))

# ---------------------------------------------------------
# 5. MAIN CONTENT & SOCRATIC INTERACTION
# ---------------------------------------------------------
st.markdown("<p class='title-glow'>Tau: Socratic Quantum Workspace</p>", unsafe_allow_html=True)
st.caption("Fostering deep analytical deduction by penalizing cognitive offloading.")

st.markdown(f"""
<div class='module-card'>
    <strong style='color:#00ADB5; font-size:1.1rem;'>Active Mission: {current_module['title']}</strong><br>
    <span style='color:#cad2c5;'>{current_module['desc']}</span>
</div>
""", unsafe_allow_html=True)

# Verification row
c1, c2 = st.columns([3, 1])
with c1:
    user_math = st.text_input("Enter derived analytical expression:", placeholder=current_module['placeholder'])
with c2:
    st.write("")
    st.write("")
    if st.button("Validate Derivation", use_container_width=True):
        if verify_answer(user_math, current_module["target_type"]):
            st.success("🎉 Quantum state verified! Derivation analytically sound.")
            st.session_state.solved = True
            st.session_state.final_score = coherence
            st.balloons()
        else:
            st.error("❌ Expression does not satisfy the boundary or eigenvalue conditions.")

st.divider()

# Message History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
if prompt := st.chat_input(f"Discuss {current_module['title']} with Tau..."):
    st.session_state.hints_used += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.chat:
            def stream_generator():
                for chunk in st.session_state.chat.send_message_stream(prompt):
                    if chunk.text:
                        yield chunk.text
            response = st.write_stream(stream_generator())
        else:
            response = f"**Socratic Hint:** Focus on the physical constraints of {current_module['title']}. What boundary condition must the wavefunction or state vector satisfy at the edges?"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
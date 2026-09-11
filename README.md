# Ω OmegaLoop: Socratic Quantum Workspace

> **Active First-Principles Socratic Workspace for Theoretical Physics | Advancing UN SDG 4 (Quality Education)**

---

## 1. Project Identity & Mission

**OmegaLoop** is inspired by angular frequency ($\omega$) and the cyclic, iterative deduction essential to theoretical physics. 

### UN SDG 4: Preventing Cognitive Offloading
Modern generative AI often causes **cognitive offloading**—where learners outsource deep mathematical reasoning and physical derivation to an AI, stunting cognitive development. 

OmegaLoop reverses this trend by enforcing:
* **First-principles reasoning**: Scaffolded deduction over passive consumption.
* **Zero-solution policy in Challenge Mode**: The AI refuses to output closed-form equations or numeric solutions, answering exclusively via tiered physical hints.
* **Active transfer validation**: Numerical explanations conclude with mandatory **"What-If" Transfer Cards** to test parameter scaling intuition.

---

## 2. Oxford Slate Light Academic Visual Language

* **App Background**: Crisp paper slate (`#F8FAFC`)
* **Sidebar & Card Containers**: Cool pale slate (`#F1F5F9`) with slate borders (`#CBD5E1`) and soft elevation shadows (`rgba(0,0,0,0.04)`)
* **Primary Branding & Action Accents**: Deep theoretical royal blue (`#2563EB`) and dark navy (`#0F172A`)
* **Decoherence Warning / Amber Accent**: Warm amber (`#B45309`) for timers and decoherence decay states
* **Fact Banner Accent**: Vibrant blue highlight (`#EFF6FF` card with `#2563EB` vertical border)
* **Mathematical Typesetting**: KaTeX auto-rendered LaTeX for quantum operators ($\hat{x}, \hat{p}$), wavefunctions ($\psi(x)$), commutator brackets ($[\hat{x}, \hat{p}] = i\hbar$), and state vectors ($|\psi\rangle$).

---

## 3. Architecture & Core Features

### 1. Left Sidebar Navigation (Gemini-Inspired)
* **Brand Header**: Animated brand mark ($\Omega$), subtitle, and active SDG 4 Anti-Offloading badge.
* **Primary Actions**: `+ New Chat` thread button and real-time history filter search.
* **Operational Mode Switcher**:
  * **Mode A: 📖 Conceptual & Numerical Tutor**
  * **Mode B: ⚡ Challenge Time (Gamified)**
* **Categorized Curriculum Tracks**:
  * **Track 1: The Foundational Triad** (Wave-Particle Duality, Quantum Superposition, Heisenberg Uncertainty)
  * **Track 2: Modern Quantum Information** (Qubits on Bloch Sphere, Bell States, Tunneling)
  * **Track 3: Historical Quantization** (Planck Blackbody, Photoelectric Effect, Bohr Model)
* **Collapsible History Drawer**:
  * Tab 1: **Recent Chats** with timestamps.
  * Tab 2: **Challenge Log** showing problem status, elapsed time, hints, and Coherence ($\tau$).
* **Visual Observatory Preview**: Mini live canvas rendering quantum probability densities $|\psi(x)|^2$.
* **User Profile Footer**: Scholar tier and settings modal.

### 2. Main Canvas & Dual-Mode Engine
* **Status Bar**: Tracks active curriculum track, current focus topic, operational mode badge, and universal quantum constants ($\hbar, c$).
* **Daily Quantum Observable Card**: Persistent highlight card presenting authentic physical facts with a rotation mechanism.
* **Mode A (Socratic Tutor)**:
  * Comprehensive analytical derivations.
  * Dedicated **1-sentence physical explanation** for *why* each mathematical step is performed.
  * Mandatory **"What-If" Transfer Card** with immediate deductive feedback.
* **Mode B (Challenge Time)**:
  * Strict Anti-Cheat Protocol (AI refuses closed-form solutions).
  * Live **Quantum Coherence Score ($\tau$)** decaying over time and hint usage.
  * Active **Countdown Timer** (05:00 countdown).
  * **Tiered Socratic Hints** (Physical Intuition $\rightarrow$ Boundary Principles $\rightarrow$ Algebraic Normalization).
  * **Solution Validation Bar**: Expression parser testing boundary and eigenvalue conditions with instant pass/fail animation.
  * **Coherence Boundary Reached (Timer Expiration Fork)**: When the timer expires (or via the test button), modal presents two paths:
    1. `⏱️ Grant +2 Extra Minutes`: Adds +120s to derive independently.
    2. `📖 Reveal Derivation & Explain`: Concludes the trial and reveals the full analytical proof with commentary.

### 3. Visual Observatory Modal
Full-screen interactive canvas allowing visualization of:
1. **Infinite Square Well** ($n = 1, 2$)
2. **Quantum Harmonic Oscillator** ($v = 0$ ground state Gaussian)
3. **Finite Barrier Tunneling** (Oscillatory interference, exponential decay, transmitted wave)

### 4. Floating Bottom Interaction Bar
* Pill-shaped floating bar anchored to the bottom with backdrop blur.
* Dynamic placeholder reflecting operational mode.
* Model badge (`Omega-Socratic Flash`) and quick inquiry chips.

---

## 4. Running the Workspace Locally

To run the frontend locally:

```bash
# Option 1: Using the included Python runner
python server.py

# Option 2: Using Python built-in HTTP server
python -m http.server 8080
```

Then visit:
```
http://localhost:8080/index.html
```
Or open `index.html` directly in any modern browser.

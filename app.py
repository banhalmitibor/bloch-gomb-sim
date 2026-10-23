import streamlit as st
import numpy as np
import plotly.graph_objects as go


class Gate:
    def __init__(self):
        self.matrix = None

    def apply(self, state):
        return np.dot(self.matrix, state)

class HadamardGate(Gate):
    def __init__(self):
        self.matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype = complex)

class PauliXGate(Gate):
    def __init__(self):
        self.matrix = np.array([[0, 1], [1, 0]], dtype = complex)

class PauliZGate(Gate):
    def __init__(self):
        self.matrix = np.array([[1, 0], [0, -1]],dtype = complex)

class PauliYGate(Gate):
    def __init__(self):
        self.matrix = np.array([[0, -1j], [1j, 0]], dtype = complex)

class PhaseSGate(Gate):
    def __init__(self):
        self.matrix = np.array([[1,0], [0,1j]], dtype = complex)

class PhaseTGate(Gate):
    def __init__(self):
        self.matrix = np.array([[1,0],[0,np.exp(1j*np.pi/4)]],dtype = complex)

class PhaseRotator(Gate):
    def __init__(self, alpha):
        self.matrix = np.array([
            [1, 0],
            [0, np.exp(1j * alpha)]
        ], dtype=complex)

class Chain(Gate):
    def __init__(self):
        self.matrixes = []

    def addMatrix(self, mx):
        self.matrixes.append(mx)

    def apply(self, state):
        mx = state
        for matrix in self.matrixes:
            mx = np.dot(matrix, mx)
        return mx
























# -- 1. ÁLLAPOTTÉR INICIALIZÁLÁSA --
if 'state' not in st.session_state:
    # Kezdőállapot: |0>
    st.session_state.state = np.array([1, 0], dtype=complex)

if 'custom_gates' not in st.session_state:
    st.session_state.custom_gates = {}

if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
    st.session_state.temp_chain = Chain()
    st.session_state.temp_names = []

# -- 2. KVANUMKAPUK (MÁTRIXOK) --
H_gate = HadamardGate()
X_gate = PauliXGate()
Z_gate = PauliZGate()
Y_gate = PauliYGate() 
S_gate = PhaseSGate()
T_gate = PhaseTGate()  

# -- 3. FELHASZNÁLÓI FELÜLET (UI) --
st.title("Bloch-gömb Szimulátor")

st.sidebar.header("Kezdőállapot beállítása")

col1, col2 = st.sidebar.columns(2)

a_re = col1.number_input("α (Valós)", value=1.0, step=0.1)
a_im = col2.number_input("α (Képzetes)", value=0.0, step=0.1)
b_re = col1.number_input("β (Valós)", value=0.0, step=0.1)
b_im = col2.number_input("β (Képzetes)", value=0.0, step=0.1)

if st.sidebar.button("Állapot beállítása"):
    alpha_val = complex(a_re, a_im)
    beta_val = complex(b_re, b_im)
    
    norm = np.sqrt(abs(alpha_val)**2 + abs(beta_val)**2)
    if norm > 0:
        alpha_val /= norm
        beta_val /= norm
        st.session_state.state = np.array([alpha_val, beta_val], dtype=complex)


if st.sidebar.button("Visszaállítás |0>-ba"):
    st.session_state.state = np.array([1, 0], dtype=complex) 



st.sidebar.header("Kvantumkapuk")

# Gombok a kapuk alkalmazásához
if st.sidebar.button("Hadamard kapu"):
    st.session_state.state = H_gate.apply(st.session_state.state)
    
if st.sidebar.button("Pauli-X kapu"):
    st.session_state.state = X_gate.apply(st.session_state.state)

if st.sidebar.button("Pauli-Z kapu"):
    st.session_state.state = Z_gate.apply(st.session_state.state)

if st.sidebar.button("Pauli-Y kapu"):
    st.session_state.state = Y_gate.apply(st.session_state.state)

if st.sidebar.button("S fáziskapu"):
    st.session_state.state = S_gate.apply(st.session_state.state)

if st.sidebar.button("T fáziskapu"):
    st.session_state.state = T_gate.apply(st.session_state.state)

alpha_value = st.sidebar.number_input(
    "Adja meg alpha értékét radiánban", 
    value=0.0,      # Default value
    step=0.1,       # Step size for the UI arrows
    format="%.4f"   # Display formatting
)
if st.sidebar.button("Phase-Rotator kapu"):
    st.session_state.state = PhaseRotator(alpha_value).apply(st.session_state.state)
  

# -- 4. VEKTOR KOORDINÁTÁINAK KISZÁMÍTÁSA --
alpha, beta = st.session_state.state

# Bloch-koordináták közvetlen kiszámítása (nincs arccos és np.angle hiba!)
x = float(2 * np.real(np.conj(alpha) * beta))
y = float(2 * np.imag(np.conj(alpha) * beta))
z = float(np.abs(alpha)**2 - np.abs(beta)**2)

# Lebegőpontos túlcsordulások védelme (-1 és 1 közé szorítás)
x = np.clip(x, -1.0, 1.0)
y = np.clip(y, -1.0, 1.0)
z = np.clip(z, -1.0, 1.0)



# Bloch-gömb koordináták konverziója (theta, phi)
#theta = 2 * np.arccos(np.abs(alpha))
#phi = np.angle(beta) - np.angle(alpha)

# Descartes-koordináták a 3D térhez
#x = np.sin(theta) * np.cos(phi)
#y = np.sin(theta) * np.sin(phi)
#z = np.cos(theta)

# -- 5. PLOTLY 3D MEGJELENÍTÉS --
fig = go.Figure()

# Halvány, átlátszó gömb hozzáadása
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
sphere_x = np.cos(u)*np.sin(v)
sphere_y = np.sin(u)*np.sin(v)
sphere_z = np.cos(v)
fig.add_trace(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, opacity=0.1, showscale=False))

# Állapotvektor kirajzolása (egy vonal az origóból a kiszámolt x,y,z pontig)
fig.add_trace(go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers',
                           line=dict(color='red', width=5),
                           marker=dict(size=[0, 5], color='red')))

# Tengelyek testreszabása
fig.update_layout(scene=dict(
    xaxis=dict(range=[-1, 1], title='X'),
    yaxis=dict(range=[-1, 1], title='Y'),
    zaxis=dict(range=[-1, 1], title='Z')),
    margin=dict(l=0, r=0, b=0, t=0))

st.plotly_chart(fig, use_container_width=True)

# Pontos állapot kiírása
st.write(f"**Aktuális állapotvektor:** |ψ⟩ = {alpha:.2f}|0⟩ + {beta:.2f}|1⟩")

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
        self.gates = []

    def addGate(self, gt):
        self.gates.append(gt)

    def apply(self, state):
        mx = state
        for gate in self.gates:
            mx = gate.apply(mx)
        return mx




def apply_or_record_gate(name, gate_obj=None):
    if st.session_state.is_recording:
        st.session_state.temp_chain.addGate(gate_obj)
        st.session_state.temp_names.append(name)
        st.rerun()
    else:
        st.session_state.state = gate_obj.apply(st.session_state.state)
    


















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

col3, col4 = st.sidebar.columns(2)

# Gombok a kapuk alkalmazásához
if col4.button("Hadamard kapu"):
    apply_or_record_gate("H", H_gate)
    
if col3.button("Pauli-X kapu"):
    apply_or_record_gate("X", X_gate)

if col3.button("Pauli-Z kapu"):
    apply_or_record_gate("Z", Z_gate)

if col3.button("Pauli-Y kapu"):
    apply_or_record_gate("Y", Y_gate)

if col4.button("S fáziskapu"):
    apply_or_record_gate("S", S_gate)

if col4.button("T fáziskapu"):
    apply_or_record_gate("T", T_gate)

col5, col6,col7 = st.sidebar.columns([1,4,1])

col6.markdown("<h5 style='text-align: center;'>Fázisszög (α)</h5>", unsafe_allow_html=True)

alpha_value = col6.slider(
"Fázisszög (α)", 
    min_value=0, 
    max_value=360, 
    value=90, 
    step=1,
    format="%d°",
    label_visibility = "collapsed"
)
angle_rad = np.radians(alpha_value)

if col6.button("Fázisforgatás",use_container_width = True):
    phase_gate = PhaseRotator(angle_rad)
    apply_or_record_gate(f"P({alpha_value:.1f})", phase_gate)
  

st.sidebar.divider()
if not st.session_state.is_recording:
    if st.sidebar.button("Új láncolt kapu rögzítése"):
        st.session_state.is_recording = True
        st.session_state.temp_chain = Chain()
        st.session_state.temp_names = []
        st.rerun()
else:
    st.sidebar.warning("Lánc rögzítése folyamatban...")
    st.sidebar.write("**Jelenlegi lánc:**", " ➔ ".join(st.session_state.temp_names) if st.session_state.temp_names else "Üres")
    
    gate_name = st.sidebar.text_input("Új kapu neve:", value=f"Lánc {len(st.session_state.custom_gates) + 1}")
    
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Mentés"):
        st.session_state.custom_gates[gate_name] = st.session_state.temp_chain
        st.session_state.is_recording = False
        st.rerun()
    if col2.button("Mégse"):
        st.session_state.is_recording = False
        st.rerun()

if st.session_state.custom_gates:
    st.sidebar.divider()
    st.sidebar.header("Saját láncolt kapuk")
    for name, chain_gate in st.session_state.custom_gates.items():
        if st.sidebar.button(name):
            # Mivel a lánc maga is egy Gate, használhatjuk hozzá a segédfüggvényt!
            apply_or_record_gate(name, chain_gate)

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

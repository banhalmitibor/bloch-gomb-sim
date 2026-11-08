import streamlit as st
import numpy as np
import plotly.graph_objects as go

# A kvantumkapuk alaposztálya, ettől örökölve fogjuk definiálni a konkrét kapukat.
class Gate:
    def __init__(self):
        self.matrix = None

    def apply(self, state):
        return np.dot(self.matrix, state)

    
# Hadamard, Pauli-X, Pauli-Z, Pauli-Y, S, T, Rz, Rx, Ry kapuk definiálása

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

class RzGate(Gate):
    def __init__(self, alpha):
        self.matrix = np.array([
            [1, 0],
            [0, np.exp(1j * alpha)]
        ], dtype=complex)

class RxGate(Gate):
    def __init__(self, theta):
        self.matrix = np.array([
            [np.cos(theta/2), -1j * np.sin(theta/2)],
            [-1j * np.sin(theta/2), np.cos(theta/2)]
        ], dtype=complex)

class RyGate(Gate):
    def __init__(self, theta):
        self.matrix = np.array([
            [np.cos(theta/2), -np.sin(theta/2)],
            [np.sin(theta/2), np.cos(theta/2)]
        ], dtype=complex)

# Láncolt kapu osztály, amely több Gate objektumot tartalmazhat és alkalmazhatja őket sorban.

class Chain(Gate):
    def __init__(self):
        self.gates = []

    # A láncolt kapuhoz új kapu hozzáadása
    def addGate(self, gt):
        self.gates.append(gt)

    # A láncba lévő kapuk alkalmazása a bemeneti állapotra
    def apply(self, state):
        mx = state
        for gate in self.gates:
            mx = gate.apply(mx)
        return mx

# Segédfüggvény a kapuk alkalmazására vagy rögzítésére a láncolt kapuhoz (session_state.is_recording  == láncolás aktív)
def apply_or_record_gate(name, gate_obj=None):
    if st.session_state.is_recording:
        st.session_state.temp_chain.addGate(gate_obj)
        st.session_state.temp_names.append(name)
        st.rerun()
    else:
        active_vc = st.session_state.active_vector
        current_state = st.session_state.vectors[active_vc]["state"]
        st.session_state.vectors[active_vc]["state"] = gate_obj.apply(current_state)

    
# Állapotvektorok lehetséges színeinek a listája
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow','violet', 'lime', 'pink', 'teal', 'brown', 'gray', 'olive', 'navy']


# Állapottér inicializálása a Streamlit session_state-ben, ha még nem létezik
if 'vectors' not in st.session_state:
    st.session_state.vectors = {
        "vc1": {
            "state": np.array([1,0],dtype=complex),
            "color": colors[0]
        }
    }
    st.session_state.active_vector = "vc1"
    st.session_state.vector_count = 1

if 'custom_gates' not in st.session_state:
    st.session_state.custom_gates = {}

if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
    st.session_state.temp_chain = Chain()
    st.session_state.temp_names = []

# Kvantumkapuk példányosítása
H_gate = HadamardGate()
X_gate = PauliXGate()
Z_gate = PauliZGate()
Y_gate = PauliYGate() 
S_gate = PhaseSGate()
T_gate = PhaseTGate()  

# Cím és oldalsáv beállításai

st.title("Bloch-gömb Szimulátor")


# Állapotvektorok kezelése UI
st.sidebar.header("Állapotvektorok kezelése")

col8, col9 = st.sidebar.columns(2)

# Váltás az állapotvektorok kijelölése közt
selected_vc = st.sidebar.selectbox(
    "Vektor kiválasztása:",
    options = list(st.session_state.vectors.keys()),
    index = list(st.session_state.vectors.keys()).index(st.session_state.active_vector)
)
st.session_state.active_vector = selected_vc

# Új állapotvektor hozzáadása
if st.sidebar.button("Új állapotvektor:"):
    st.session_state.vector_count += 1

    uj_vektor = f"vc{st.session_state.vector_count}"

    st.session_state.vectors[uj_vektor] = {
        "state" : np.array([1,0],dtype = complex),
        "color" : colors[(st.session_state.vector_count-1) % len(colors)]
    }
    st.session_state.active_vector = uj_vektor
    st.rerun()

# Kezdőállapot beállítása UI
st.sidebar.header("Kezdőállapot beállítása")

col1, col2 = st.sidebar.columns(2)

# Lehetséges értékek beállítása 
a_re = col1.number_input("α (Valós)", value=1.0, step=0.1)
a_im = col2.number_input("α (Képzetes)", value=0.0, step=0.1)
b_re = col1.number_input("β (Valós)", value=0.0, step=0.1)
b_im = col2.number_input("β (Képzetes)", value=0.0, step=0.1)

# A beállított értékek normalizálása és az állapotvektor frissítése
if st.sidebar.button("Állapot beállítása"):
    alpha_val = complex(a_re, a_im)
    beta_val = complex(b_re, b_im)
    
    norm = np.sqrt(abs(alpha_val)**2 + abs(beta_val)**2)
    if norm > 0:
        alpha_val /= norm
        beta_val /= norm
        st.session_state.vectors[st.session_state.active_vector]["state"] = np.array([alpha_val, beta_val], dtype=complex)

# Az állapotvektor visszaállítása |0>-ba 
if st.sidebar.button("Visszaállítás |0>-ba"):
    st.session_state.vectors[st.session_state.active_vector]["state"] = np.array([1, 0], dtype=complex) 


# Kvantumkapuk UI
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

st.sidebar.divider()

# A forgatási szög és tengely kiválasztása a forgatási kapukhoz
st.sidebar.header("Tengely körüli forgatások")
axis = st.sidebar.radio("Tengely kiválasztása", ["X tengely (Rx)", "Y tengely (Ry)", "Z tengely (Rz)"], horizontal=True, label_visibility="collapsed")

angle = st.sidebar.slider("Forgatási szög", min_value=0, max_value=360, value=90, step=1, format="%d°", label_visibility="collapsed")

if st.sidebar.button("Forgatás alkalmazása", use_container_width=True):
    rad = np.radians(angle)
    if "X" in axis:
        apply_or_record_gate(f"Rx({angle}°)", RxGate(rad))
    elif "Y" in axis:
        apply_or_record_gate(f"Ry({angle}°)", RyGate(rad))
    else:
        apply_or_record_gate(f"Rz({angle}°)", RzGate(rad)) 

st.sidebar.divider()

# Láncolt kapuk kezelése UI
st.sidebar.header("Láncolt kapuk kezelése")

# Láncolt kapu rögzítése és mentése
if not st.session_state.is_recording:
    if st.sidebar.button("Új láncolt kapu rögzítése"):
        st.session_state.is_recording = True
        st.session_state.temp_chain = Chain()
        st.session_state.temp_names = []
        st.rerun()
else:
    st.sidebar.warning("Lánc rögzítése folyamatban...")
    st.sidebar.write("**Jelenlegi lánc:**", " ➔ ".join(st.session_state.temp_names) if st.session_state.temp_names else "Üres")

    # A rögzített kapuk nevének megadása
    gate_name = st.sidebar.text_input("Új kapu neve:", value=f"Lánc {len(st.session_state.custom_gates) + 1}")
    
    col1, col2 = st.sidebar.columns(2)

    # Gombok a láncolt kapu mentéséhez vagy elvetéséhez
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
            # (A lánc maga is egy Gate objektum, így közvetlenül alkalmazható)
            apply_or_record_gate(name, chain_gate)

# Megjelenítés plotly segítségével
fig = go.Figure()

# Halvány, átlátszó gömb hozzáadása
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
sphere_x = np.cos(u)*np.sin(v)
sphere_y = np.sin(u)*np.sin(v)
sphere_z = np.cos(v)
fig.add_trace(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, opacity=0.1, showscale=False))

# Állapotvektorok kirajzolása a Bloch-gömbön

# Alfa és béta komponensek kinyerése az állapotvektorokból
for vector_key, vector_value in st.session_state.vectors.items():
    alpha, beta = st.session_state.vectors[vector_key]["state"]

# Bloch-koordináták kiszámítása az állapotvektorból
    x = float(2 * np.real(np.conj(alpha) * beta))
    y = float(2 * np.imag(np.conj(alpha) * beta))
    z = float(np.abs(alpha)**2 - np.abs(beta)**2)

# Lebegőpontos túlcsordulások védelme (-1 és 1 közé szorítás)
    x = np.clip(x, -1.0, 1.0)
    y = np.clip(y, -1.0, 1.0)
    z = np.clip(z, -1.0, 1.0)
    
# Állapotvektorok kirajzolása a Bloch-gömbön, az aktív vektort vastagabb vonallal és nagyobb ponttal jelöljük
    if vector_key == st.session_state.active_vector:
        st.write(f"**Aktív állapotvektor: {vector_key}** |ψ⟩ = {alpha:.2f}|0⟩ + {beta:.2f}|1⟩")
        fig.add_trace(go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers',
                           line=dict(color=vector_value["color"], width=7),
                           marker=dict(size=[0, 6], color=vector_value["color"]),name = f"Aktív: {vector_key}"))
    else:
         fig.add_trace(go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers',
                           line=dict(color=vector_value["color"], width=3),
                           marker=dict(size=[0, 4], color=vector_value["color"]),name = vector_key))

# Tengelyek testreszabása
    fig.update_layout(scene=dict(
        xaxis=dict(range=[-1, 1], title='X'),
        yaxis=dict(range=[-1, 1], title='Y'),
        zaxis=dict(range=[-1, 1], title='Z')),
        margin=dict(l=0, r=0, b=0, t=0))

# A Bloch-gömb megjelenítése a Streamlit alkalmazásban
st.plotly_chart(fig, use_container_width=True)
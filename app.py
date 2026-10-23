import streamlit as st
import numpy as np
import plotly.graph_objects as go


class Gate:
    def __init__(self):
        self.matrix = None

    def apply(self, state):
        return np.dot(self.matrix, state)

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

# -- 2. KVANUMKAPUK (MÁTRIXOK) --
H_gate = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
X_gate = np.array([[0, 1], [1, 0]])

# -- 3. FELHASZNÁLÓI FELÜLET (UI) --
st.title("Bloch-gömb Szimulátor")
st.sidebar.header("Kvantumkapuk")

# Gombok a kapuk alkalmazásához
if st.sidebar.button("Hadamard (H) kapu"):
    st.session_state.state = np.dot(H_gate, st.session_state.state)
    print("8=====================================D")

if st.sidebar.button("Pauli-X (NOT) kapu"):
    st.session_state.state = np.dot(X_gate, st.session_state.state)

if st.sidebar.button("Visszaállítás |0>-ba"):
    st.session_state.state = np.array([1, 0], dtype=complex)    

# -- 4. VEKTOR KOORDINÁTÁINAK KISZÁMÍTÁSA --
alpha, beta = st.session_state.state
# Bloch-gömb koordináták konverziója (theta, phi)
theta = 2 * np.arccos(np.abs(alpha))
phi = np.angle(beta) - np.angle(alpha)

# Descartes-koordináták a 3D térhez
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

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

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Perceptrón Gamificado", layout="wide")

st.title("🎮 Tarea 1: Perceptrón Gamificado")
st.markdown("""
Ajusta manualmente las **perillas (pesos)** para clasificar los patrones. 
Recuerda: El objetivo es que la línea (frontera de decisión) separe los puntos positivos de los negativos.
""")

# --- Sidebar: Configuración de Datos ---
st.sidebar.header("Configuración de Entradas")
combinations = [(0,0), (0,1), (1,0), (1,1)]
targets = []

st.sidebar.subheader("Define las etiquetas (Deseado)")
for i, combo in enumerate(combinations):
    col1, col2 = st.sidebar.columns([1, 1])
    col1.write(f"Entrada {combo}:")
    target = col2.selectbox(f"Clase", ["Negativo (-1)", "Positivo (1)"], key=f"target_{i}")
    targets.append(1 if "Positivo" in target else -1)

# --- Controles de Pesos (Las Perillas) ---
st.header("Perillas de Ajuste Manual")
col_w1, col_w2, col_b = columns = st.columns(3)

w1 = col_w1.select_slider("Peso W1", options=np.round(np.arange(-2.0, 2.1, 0.1), 2), value=0.0)
w2 = col_w2.select_slider("Peso W2", options=np.round(np.arange(-2.0, 2.1, 0.1), 2), value=0.0)
bias = col_b.select_slider("Bias (Umbral)", options=np.round(np.arange(-2.0, 2.1, 0.1), 2), value=0.0)

# --- Cálculos del Perceptrón ---
def perceptron(x1, x2, w1, w2, b):
    z = (x1 * w1) + (x2 * w2) + b
    y = 1 if z >= 0 else -1
    return z, y

results = []
correct_count = 0

for i, (x1, x2) in enumerate(combinations):
    z, y = perceptron(x1, x2, w1, w2, bias)
    is_correct = y == targets[i]
    if is_correct:
        correct_count += 1
    results.append({"Combo": (x1, x2), "Z (Suma)": round(z, 2), "Salida": y, "Deseada": targets[i], "Correcto": is_correct})

# --- Visualización ---
col_grafica, col_tabla = st.columns([2, 1])

with col_grafica:
    # Crear Frontera de Decisión: w1*x1 + w2*x2 + b = 0  => x2 = (-w1*x1 - b) / w2
    fig = go.Figure()

    # Puntos de datos
    for i, res in enumerate(results):
        color = 'blue' if res["Deseada"] == 1 else 'red'
        symbol = 'circle' if res["Correcto"] else 'x'
        fig.add_trace(go.Scatter(x=[res["Combo"][0]], y=[res["Combo"][1]], 
                                 mode='markers', marker=dict(color=color, size=15, symbol=symbol),
                                 name=f"In {res['Combo']}"))

    # Dibujar Línea de decisión
    if w2 != 0:
        x_vals = np.array([-0.5, 1.5])
        y_vals = (-w1 * x_vals - bias) / w2
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Frontera', line=dict(color='green', dash='dash')))
    elif w1 != 0: # Caso línea vertical
        x_val = -bias / w1
        fig.add_vline(x=x_val, line_dash="dash", line_color="green")

    fig.update_layout(xaxis_range=[-0.5, 1.5], yaxis_range=[-0.5, 1.5], title="Plano 2D y Frontera de Decisión")
    st.plotly_chart(fig, use_container_width=True)

with col_tabla:
    st.subheader("Métricas")
    st.metric("Patrones Correctos", f"{correct_count}/4")
    st.table(results)

st.success(f"Puntaje de clasificación: {(correct_count/4)*100}%")

import streamlit as st
import numpy as np
from scipy.stats import norm, t

st.title("Kalkulator przedziałów ufności")

# INPUT
n = st.number_input("Liczebność próby (n)", min_value=1, value=30)
mean = st.number_input("Średnia (x̄)", value=10.0)
std = st.number_input("Odchylenie standardowe", value=2.0)

std_type = st.radio(
    "Rodzaj odchylenia:",
    ["Z populacji (σ)", "Z próby (s)"]
)

confidence = st.slider("Poziom ufności (%)", 80, 99, 95)

# OBLICZENIA
alpha = 1 - confidence / 100

if std_type == "Z populacji (σ)":
    z = norm.ppf(1 - alpha / 2)
    margin = z * (std / np.sqrt(n))
    dist_symbol = "z"
else:
    t_val = t.ppf(1 - alpha / 2, df=n-1)
    margin = t_val * (std / np.sqrt(n))
    dist_symbol = "t"

lower = mean - margin
upper = mean + margin

# WYNIK
st.subheader("📊 Wynik")

st.latex(r"\bar{x} = " + str(mean))
st.latex(r"n = " + str(n))
st.latex(r"s/\sigma = " + str(std))

if dist_symbol == "z":
    st.latex(r"CI = \bar{x} \pm z \cdot \frac{\sigma}{\sqrt{n}}")
    st.latex(
        rf"{mean} \pm {z:.3f} \cdot \frac{{{std}}}{{\sqrt{{{n}}}}}"
    )
else:
    st.latex(r"CI = \bar{x} \pm t \cdot \frac{s}{\sqrt{n}}")
    st.latex(
        rf"{mean} \pm {t_val:.3f} \cdot \frac{{{std}}}{{\sqrt{{{n}}}}}"
    )

st.success(f"Przedział ufności: ({lower:.3f}, {upper:.3f})")

import streamlit as st
import numpy as np
from scipy.stats import norm, t

st.set_page_config(page_title="Przedziały ufności", layout="centered")

st.title("📊 Kalkulator przedziałów ufności")

st.markdown("""
Obliczanie przedziału ufności dla średniej.

**Zasady:**
- σ znane → rozkład normalny (Z)
- σ nieznane i n ≥ 30 → rozkład normalny (Z)
- σ nieznane i n < 30 → rozkład t-Studenta
""")

# ======================
# INPUT
# ======================

st.header("🔢 Dane wejściowe")

col1, col2 = st.columns(2)

with col1:
    n = st.number_input("Liczebność próby (n)", min_value=1, value=30)
    mean = st.number_input("Średnia (x̄)", value=10.0)

with col2:
    std = st.number_input("Odchylenie standardowe", value=2.0)
    std_type = st.radio(
        "Rodzaj odchylenia:",
        ["Znane σ (populacja)", "Nieznane σ (próba - s)"]
    )
    confidence = st.slider("Poziom ufności (%)", 80, 99, 95)

alpha = 1 - confidence / 100

# ======================
# WYBÓR ROZKŁADU
# ======================

if std_type == "Znane σ (populacja)":
    crit_value = norm.ppf(1 - alpha / 2)
    margin = crit_value * (std / np.sqrt(n))
    dist = "Z"
    symbol = r"\sigma"

elif n >= 30:
    crit_value = norm.ppf(1 - alpha / 2)
    margin = crit_value * (std / np.sqrt(n))
    dist = "Z"
    symbol = "s"

else:
    crit_value = t.ppf(1 - alpha / 2, df=n - 1)
    margin = crit_value * (std / np.sqrt(n))
    dist = "t"
    symbol = "s"

lower = mean - margin
upper = mean + margin

# ======================
# WYNIK
# ======================

st.header("📈 Wynik")

if dist == "Z":
    st.markdown("**Użyto rozkładu normalnego (Z)**")
    st.latex(
        rf"\left( \bar{{X}} \pm u_{{1-\frac{{\alpha}}{{2}}}} \cdot \frac{{{symbol}}}{{\sqrt{{n}}}} \right)"
    )
else:
    st.markdown("**Użyto rozkładu t-Studenta**")
    st.latex(
        rf"\left( \bar{{X}} \pm t_{{1-\frac{{\alpha}}{{2}}, n-1}} \cdot \frac{{s}}{{\sqrt{{n}}}} \right)"
    )

st.markdown("---")
st.info("""
📌 Interpretacja:
- Jeśli znane jest σ → używamy rozkładu normalnego
- Jeśli σ nieznane:
    - dla dużych prób (n ≥ 30) → aproksymacja normalna
    - dla małych prób → rozkład t-Studenta
""")

# ======================
# KROKI OBLICZEŃ
# ======================

st.subheader("📘 Kroki obliczeń")

# Krok 1
st.markdown("### 1️⃣ Dane")
st.latex(rf"n = {n}")
st.latex(rf"\bar{{x}} = {mean}")
st.latex(rf"{symbol} = {std}")
st.latex(rf"\alpha = {alpha:.3f}")

# Krok 2
st.markdown("### 2️⃣ Wartość krytyczna")

if dist == "Z":
    st.latex(rf"u_{{1-\frac{{\alpha}}{{2}}}} = {crit_value:.3f}")
else:
    st.latex(rf"t_{{1-\frac{{\alpha}}{{2}}, {n-1}}} = {crit_value:.3f}")

# Krok 3
st.markdown("### 3️⃣ Podstawienie")

st.latex(
    rf"{mean} \pm {crit_value:.3f} \cdot \frac{{{std}}}{{\sqrt{{{n}}}}}"
)

# Krok 4
st.markdown("### 4️⃣ Wynik")

st.latex(
    rf"({mean:.3f} - {margin:.3f},\ {mean:.3f} + {margin:.3f})"
)

st.success(f"Przedział ufności: ({lower:.3f}, {upper:.3f})")

# ◈ Root Finding Calculator

> GUI-based Nonlinear Equation Solver
> Bisection · Newton-Raphson · Secant · Regula Falsi

---

## 📦 Requirements

```bash
pip install matplotlib numpy sympy
```
> Tkinter comes built-in with Python — no extra install needed!

---

## 🚀 How to Run

```bash
python root_finder.py
```

A full desktop window will open instantly.

---

## 🔢 How to Use

1. **Enter your equation** in the input box (e.g. `x**3 - x - 2`)
2. **Select a method** (or "Compare All" to run all 4)
3. **Set parameters** (interval a,b or starting point x0)
4. Click **▶ SOLVE**
5. View results across 4 tabs!

---

## ✍️ Equation Syntax

| Math         | Type in app     |
|---|---|
| x³ - x - 2  | `x**3 - x - 2`  |
| cos(x) - x  | `cos(x) - x`    |
| eˣ - 3x     | `exp(x) - 3*x`  |
| √x - 2      | `sqrt(x) - 2`   |
| ln(x) - 1   | `log(x) - 1`    |
| x² - 4      | `x**2 - 4`      |

---

## 🔍 Methods Explained

| Method | Best For | Speed |
|---|---|---|
| Bisection | Always reliable, needs interval | Slow |
| Newton-Raphson | Fast convergence, needs x0 | Very Fast |
| Secant | No derivative needed | Fast |
| Regula Falsi | Stable + interval-based | Medium |

---

## 📊 Dashboard Tabs

- **📈 Function Graph** — Equation plotted with root(s) marked
- **📋 Iteration Table** — Every step with values and error
- **📉 Convergence** — Error reduction per iteration (log scale)
- **⚖ Compare All** — Side-by-side bar charts of all methods

---

## 📁 Project Structure

```
root_finder/
├── root_finder.py     ← Run this file
└── README.md          ← This guide
```

"""
╔══════════════════════════════════════════════════╗
║    ROOT FINDING CALCULATOR — JUPYTER VERSION     ║
║  Bisection · Newton-Raphson · Secant · Reg-Falsi ║
╚══════════════════════════════════════════════════╝

Run in Jupyter Notebook or Google Colab.
First install: pip install ipywidgets matplotlib numpy sympy
"""

# ── Install check ──────────────────────────────────
import subprocess, sys
for pkg in ["ipywidgets","matplotlib","numpy","sympy"]:
    subprocess.run([sys.executable,"-m","pip","install",pkg,"-q"])

# ── Imports ────────────────────────────────────────
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Rectangle
import ipywidgets as widgets
from IPython.display import display, clear_output
import warnings
warnings.filterwarnings("ignore")

# ── Dark Theme Setup ───────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0D1117",
    "axes.facecolor":    "#161B22",
    "axes.edgecolor":    "#30363D",
    "text.color":        "#E6EDF3",
    "axes.labelcolor":   "#8B949E",
    "xtick.color":       "#8B949E",
    "ytick.color":       "#8B949E",
    "grid.color":        "#30363D",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
    "font.family":       "monospace",
    "legend.facecolor":  "#161B22",
    "legend.edgecolor":  "#30363D",
})

BG   = "#0D1117"; CARD = "#161B22"; INP  = "#21262D"; BDR  = "#30363D"
BLUE = "#58A6FF"; GRN  = "#3FB950"; RED  = "#FF6B6B"; YLW  = "#FFD93D"
ORG  = "#FFA657"; PRP  = "#D2A8FF"; TXT  = "#E6EDF3"; GRY  = "#8B949E"
ACC  = "#1F6FEB"

METHOD_COLORS = {
    "Bisection":      GRN,
    "Newton-Raphson": BLUE,
    "Secant":         YLW,
    "Regula Falsi":   ORG,
}

# ══════════════════════════════════════════════════
#  ROOT FINDING ALGORITHMS
# ══════════════════════════════════════════════════

def parse_eq(expr_str):
    x    = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    f    = sp.lambdify(x, expr, 'numpy')
    df   = sp.lambdify(x, sp.diff(expr, x), 'numpy')
    return f, df

def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("❌ f(a) and f(b) must have opposite signs!\n   Check your interval [a, b].")
    hist = []
    for i in range(1, max_iter+1):
        c  = (a + b) / 2.0
        fc = f(c)
        err = abs(b - a) / 2.0
        hist.append({"Iter":i, "a":a, "b":b, "c (midpoint)":c, "f(c)":fc, "Error":err})
        if err < tol or fc == 0: break
        if f(a) * fc < 0: b = c
        else:              a = c
    return c, hist

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    hist = []
    x = x0
    for i in range(1, max_iter+1):
        fx  = f(x); dfx = df(x)
        if abs(dfx) < 1e-12:
            raise ValueError("❌ Derivative is zero!\n   Try a different starting point x₀.")
        xn  = x - fx/dfx
        err = abs(xn - x)
        hist.append({"Iter":i, "x":x, "f(x)":fx, "f'(x)":dfx, "x_new":xn, "Error":err})
        x = xn
        if err < tol: break
    return x, hist

def secant(f, x0, x1, tol=1e-6, max_iter=100):
    hist = []
    for i in range(1, max_iter+1):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-12:
            raise ValueError("❌ Division by zero in Secant!\n   Try different starting points.")
        x2  = x1 - f1*(x1-x0)/(f1-f0)
        err = abs(x2 - x1)
        hist.append({"Iter":i, "x0":x0, "x1":x1, "x2 (new)":x2, "f(x2)":f(x2), "Error":err})
        x0, x1 = x1, x2
        if err < tol: break
    return x2, hist

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("❌ f(a) and f(b) must have opposite signs!\n   Check your interval [a, b].")
    hist = []
    for i in range(1, max_iter+1):
        fa, fb = f(a), f(b)
        c  = b - fb*(b-a)/(fb-fa)
        fc = f(c)
        err = abs(fc)
        hist.append({"Iter":i, "a":a, "b":b, "c":c, "f(c)":fc, "Error":err})
        if err < tol: break
        if fa * fc < 0: b = c
        else:           a = c
    return c, hist


# ══════════════════════════════════════════════════
#  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════

def plot_function_graph(f, expr_str, results, ax_range):
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    a_plot, b_plot = ax_range[0]-1, ax_range[1]+1
    xv = np.linspace(a_plot, b_plot, 800)
    try:
        yv = f(xv)
        yv = np.where(np.abs(yv) > 1e4, np.nan, yv)
    except:
        yv = np.zeros_like(xv)

    ax.plot(xv, yv, color=BLUE, lw=2.2, label=f"f(x) = {expr_str}")
    ax.axhline(0, color=BDR, lw=1.2)
    ax.axvline(0, color=BDR, lw=0.8)

    for m, (root, _) in results.items():
        if root is not None:
            col = METHOD_COLORS.get(m, GRN)
            ax.axvline(root, color=col, lw=1.2, ls="--", alpha=0.6)
            ax.scatter([root], [0], color=col, s=140, zorder=6,
                       label=f"{m}: x = {root:.6f}",
                       edgecolors=BG, linewidths=1.8)

    y_rng = np.nanmax(np.abs(yv)) if not np.all(np.isnan(yv)) else 10
    ax.set_ylim(-y_rng*1.2, y_rng*1.2)
    ax.set_title(f"  📈  Function Graph — f(x) = {expr_str}",
                 color=TXT, fontsize=11, loc="left")
    ax.set_xlabel("x"); ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.5)
    ax.legend(fontsize=9, labelcolor="white")
    for s in ax.spines.values(): s.set_edgecolor(BDR)
    plt.tight_layout()
    plt.show()

def plot_convergence(results):
    fig, ax = plt.subplots(figsize=(11, 4.5))
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    plotted = False
    for m, (root, hist) in results.items():
        if root is not None and hist:
            errors = [max(h["Error"], 1e-15) for h in hist]
            col    = METHOD_COLORS.get(m, GRN)
            ax.semilogy(range(1, len(errors)+1), errors,
                        color=col, lw=2.2, marker="o",
                        markersize=5, label=f"{m}  ({len(errors)} iters)")
            plotted = True

    if plotted:
        ax.set_title("  📉  Convergence — Error per Iteration (log scale)",
                     color=TXT, fontsize=11, loc="left")
        ax.set_xlabel("Iteration"); ax.set_ylabel("Error (log scale)")
        ax.grid(True, alpha=0.5)
        ax.legend(fontsize=9, labelcolor="white")
    for s in ax.spines.values(): s.set_edgecolor(BDR)
    plt.tight_layout()
    plt.show()

def plot_comparison(results):
    valid = {m:(r,h) for m,(r,h) in results.items()
             if r is not None and h}
    if not valid: return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.patch.set_facecolor(CARD)
    fig.suptitle("  ⚖  Method Comparison", color=TXT,
                 fontsize=12, ha="left", x=0.04)

    ns    = list(valid.keys())
    iters = [len(v[1]) for v in valid.values()]
    ferrs = [v[1][-1]["Error"] for v in valid.values()]
    cols  = [METHOD_COLORS.get(n, GRN) for n in ns]

    for ax in axes:
        ax.set_facecolor(CARD)
        ax.grid(True, alpha=0.4, axis="y")
        for s in ax.spines.values(): s.set_edgecolor(BDR)

    b1 = axes[0].bar(ns, iters, color=cols, alpha=0.85, width=0.5)
    for bar, v in zip(b1, iters):
        axes[0].text(bar.get_x()+bar.get_width()/2,
                     bar.get_height()+0.15, str(v),
                     ha="center", color="white",
                     fontweight="bold", fontsize=10)
    axes[0].set_title("Iterations to Converge", color=TXT)
    axes[0].set_ylabel("Iterations", color=GRY)
    axes[0].tick_params(axis="x", rotation=10, labelsize=9)

    b2 = axes[1].bar(ns, ferrs, color=cols, alpha=0.85, width=0.5)
    for bar, v in zip(b2, ferrs):
        axes[1].text(bar.get_x()+bar.get_width()/2,
                     bar.get_height(), f"{v:.1e}",
                     ha="center", va="bottom",
                     color="white", fontsize=8)
    axes[1].set_yscale("log")
    axes[1].set_title("Final Error", color=TXT)
    axes[1].set_ylabel("Error (log)", color=GRY)
    axes[1].tick_params(axis="x", rotation=10, labelsize=9)

    plt.tight_layout()
    plt.show()

def print_table(hist, method):
    if not hist: return
    col   = METHOD_COLORS.get(method, GRN)
    keys  = list(hist[0].keys())
    width = 14
    line  = "─" * (width * len(keys) + len(keys) + 1)

    print(f"\n  📋  Iteration Table — {method}")
    print(f"  {line}")
    header = "  │" + "│".join(f" {k:>{width-1}}" for k in keys) + "│"
    print(header)
    print(f"  {line}")
    for row in hist:
        vals = []
        for v in row.values():
            if isinstance(v, float):
                vals.append(f"{v:.8f}" if 0.0001 <= abs(v) < 1e8 else f"{v:.4e}")
            else:
                vals.append(str(v))
        print("  │" + "│".join(f" {v:>{width-1}}" for v in vals) + "│")
    print(f"  {line}\n")


# ══════════════════════════════════════════════════
#  RESULT SUMMARY
# ══════════════════════════════════════════════════

def print_summary(results, expr_str):
    print("\n" + "═"*55)
    print(f"  ◈  RESULTS — f(x) = {expr_str}")
    print("═"*55)
    for m, (root, hist) in results.items():
        sym = "✔" if root is not None else "✘"
        if root is not None:
            iters   = len(hist)
            last_e  = hist[-1]["Error"]
            print(f"\n  {sym}  {m}")
            print(f"      Root     : x  ≈  {root:.10f}")
            print(f"      Iters    :       {iters}")
            print(f"      Error    :       {last_e:.4e}")
        else:
            print(f"\n  {sym}  {m}  →  FAILED: {hist}")
    print("\n" + "═"*55)


# ══════════════════════════════════════════════════
#  MAIN SOLVER FUNCTION
# ══════════════════════════════════════════════════

def run_solver(expr_str, method, a, b, x0, sc_x0, sc_x1, tol, max_it):
    print(f"\n  ⏳  Solving f(x) = {expr_str}  using  {method}...")
    try:
        f, df = parse_eq(expr_str)
        # Quick sanity check
        f(0.0)
    except Exception as e:
        print(f"\n  ❌  Invalid equation: {e}")
        print("      Example format:  x**3 - x - 2")
        return

    results = {}
    errors  = {}

    def run(name, func):
        try:
            r, h = func()
            results[name] = (r, h)
        except Exception as e:
            results[name] = (None, str(e))
            errors[name]  = str(e)

    if method in ("Bisection", "Compare All"):
        run("Bisection",      lambda: bisection(f, a, b, tol, max_it))
    if method in ("Newton-Raphson", "Compare All"):
        run("Newton-Raphson", lambda: newton_raphson(f, df, x0, tol, max_it))
    if method in ("Secant", "Compare All"):
        run("Secant",         lambda: secant(f, sc_x0, sc_x1, tol, max_it))
    if method in ("Regula Falsi", "Compare All"):
        run("Regula Falsi",   lambda: regula_falsi(f, a, b, tol, max_it))

    if errors:
        print("\n  ⚠  Some methods encountered errors:")
        for m, e in errors.items():
            print(f"      • {m}: {e}")

    valid = {m:(r,h) for m,(r,h) in results.items() if r is not None}
    if not valid:
        print("\n  ❌  All methods failed. Check your equation and parameters.")
        return

    # ── Print Summary ──
    print_summary(results, expr_str)

    # ── Iteration Table (for single method only) ──
    if method != "Compare All":
        r, h = list(results.values())[0]
        if h and isinstance(h, list):
            print_table(h, method)

    # ── Plots ──
    ax_range = (min(a, x0, sc_x0), max(b, x0+2, sc_x1))
    plot_function_graph(f, expr_str, valid, ax_range)
    plot_convergence(valid)
    if method == "Compare All" and len(valid) > 1:
        plot_comparison(valid)


# ══════════════════════════════════════════════════
#  INTERACTIVE WIDGET UI
# ══════════════════════════════════════════════════

def launch_calculator():

    # ── Style ──
    style_lbl = {"description_width": "140px"}
    lay_full  = widgets.Layout(width="420px")
    lay_half  = widgets.Layout(width="200px")
    lay_btn   = widgets.Layout(width="420px", height="42px")

    # ── Header ──
    header = widgets.HTML("""
    <div style="
        background:#161B22;border:1px solid #30363D;
        border-radius:8px;padding:14px 20px;margin-bottom:12px;">
      <span style="color:#58A6FF;font-family:monospace;font-size:17px;font-weight:bold;">
        ◈  ROOT FINDING CALCULATOR
      </span><br>
      <span style="color:#8B949E;font-family:monospace;font-size:11px;">
        Bisection &nbsp;·&nbsp; Newton-Raphson &nbsp;·&nbsp; Secant &nbsp;·&nbsp; Regula Falsi
      </span>
    </div>""")

    # ── Equation ──
    eq_label = widgets.HTML(
        '<span style="color:#8B949E;font-family:monospace;'
        'font-size:12px;">  📐  Enter Equation  f(x) = 0</span>')
    eq_input = widgets.Text(
        value="x**3 - x - 2",
        placeholder="e.g.  cos(x) - x",
        layout=lay_full,
        style={"description_width":"0px"})

    # Quick examples
    ex_label = widgets.HTML(
        '<span style="color:#8B949E;font-family:monospace;'
        'font-size:11px;">  Quick Examples:</span>')
    examples = {
        "x³-x-2":   "x**3 - x - 2",
        "cos(x)-x": "cos(x) - x",
        "eˣ-3x":    "exp(x) - 3*x",
        "x²-4":     "x**2 - 4",
        "√x-2":     "sqrt(x) - 2",
        "sin(x)-x/2":"sin(x) - x/2",
    }
    ex_btns = []
    for label, eq in examples.items():
        btn = widgets.Button(
            description=label,
            layout=widgets.Layout(width="100px", height="30px"),
            style={"button_color": INP})
        btn.on_click(lambda b, e=eq: eq_input.__setattr__("value", e))
        ex_btns.append(btn)
    ex_row = widgets.HBox(ex_btns)

    # ── Method ──
    method_label = widgets.HTML(
        '<span style="color:#8B949E;font-family:monospace;'
        'font-size:12px;">  ⚙  Select Method</span>')
    method_dd = widgets.Dropdown(
        options=["Bisection","Newton-Raphson","Secant","Regula Falsi","Compare All"],
        value="Bisection",
        layout=lay_full,
        style=style_lbl)

    # ── Parameters ──
    param_label = widgets.HTML(
        '<span style="color:#8B949E;font-family:monospace;'
        'font-size:12px;">  🔢  Parameters</span>')

    w_a    = widgets.FloatText(value=-2,   description="Interval  a =", layout=lay_half, style=style_lbl)
    w_b    = widgets.FloatText(value=3,    description="Interval  b =", layout=lay_half, style=style_lbl)
    w_x0   = widgets.FloatText(value=1.5,  description="Start  x₀ =",   layout=lay_half, style=style_lbl)
    w_sx0  = widgets.FloatText(value=1.0,  description="Secant x₀ =",   layout=lay_half, style=style_lbl)
    w_sx1  = widgets.FloatText(value=2.0,  description="Secant x₁ =",   layout=lay_half, style=style_lbl)
    w_tol  = widgets.FloatText(value=1e-6, description="Tolerance =",   layout=lay_half, style=style_lbl)
    w_mit  = widgets.IntText(  value=100,  description="Max Iter  =",   layout=lay_half, style=style_lbl)

    param_box = widgets.VBox([])

    def update_params(change=None):
        m = method_dd.value
        if m == "Bisection":
            param_box.children = [widgets.HBox([w_a, w_b]), widgets.HBox([w_tol, w_mit])]
        elif m == "Newton-Raphson":
            param_box.children = [widgets.HBox([w_x0]),     widgets.HBox([w_tol, w_mit])]
        elif m == "Secant":
            param_box.children = [widgets.HBox([w_sx0, w_sx1]), widgets.HBox([w_tol, w_mit])]
        elif m == "Regula Falsi":
            param_box.children = [widgets.HBox([w_a, w_b]), widgets.HBox([w_tol, w_mit])]
        elif m == "Compare All":
            param_box.children = [
                widgets.HBox([w_a, w_b]),
                widgets.HBox([w_x0]),
                widgets.HBox([w_sx0, w_sx1]),
                widgets.HBox([w_tol, w_mit])
            ]

    method_dd.observe(update_params, names="value")
    update_params()

    # ── Buttons ──
    solve_btn = widgets.Button(
        description="▶  SOLVE",
        button_style="",
        layout=lay_btn,
        style={"button_color": ACC, "font_weight":"bold", "font_size":"14px"})

    clear_btn = widgets.Button(
        description="✕  CLEAR",
        layout=widgets.Layout(width="420px", height="34px"),
        style={"button_color": INP})

    output = widgets.Output()

    def on_solve(b):
        with output:
            clear_output(wait=True)
            run_solver(
                expr_str = eq_input.value.strip(),
                method   = method_dd.value,
                a        = w_a.value,
                b        = w_b.value,
                x0       = w_x0.value,
                sc_x0    = w_sx0.value,
                sc_x1    = w_sx1.value,
                tol      = w_tol.value,
                max_it   = w_mit.value,
            )

    def on_clear(b):
        with output:
            clear_output()
        eq_input.value = "x**3 - x - 2"

    solve_btn.on_click(on_solve)
    clear_btn.on_click(on_clear)

    # ── Assemble UI ──
    divider = widgets.HTML(
        '<hr style="border:0;border-top:1px solid #30363D;margin:6px 0;">')

    ui = widgets.VBox([
        header,
        eq_label, eq_input,
        ex_label, ex_row,
        divider,
        method_label, method_dd,
        divider,
        param_label, param_box,
        divider,
        solve_btn, clear_btn,
        output
    ], layout=widgets.Layout(
        padding="16px",
        background_color=CARD,
        border="1px solid #30363D",
        border_radius="10px",
        max_width="500px"
    ))

    display(ui)
    print("  ✅  Calculator loaded!  Enter equation & press SOLVE.")


# ══════════════════════════════════════════════════
#  LAUNCH
# ══════════════════════════════════════════════════
launch_calculator()

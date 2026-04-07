"""
╔══════════════════════════════════════════════════╗
║       ROOT FINDING CALCULATOR — GUI APP          ║
║  Bisection · Newton-Raphson · Secant · Reg-Falsi ║
╚══════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────
#  DARK THEME COLORS
# ─────────────────────────────────────────────────
BG_DARK    = "#0D1117"
BG_CARD    = "#161B22"
BG_INPUT   = "#21262D"
BORDER     = "#30363D"
BLUE       = "#58A6FF"
GREEN      = "#3FB950"
RED        = "#FF6B6B"
YELLOW     = "#FFD93D"
PURPLE     = "#D2A8FF"
ORANGE     = "#FFA657"
TEXT_WHITE = "#E6EDF3"
TEXT_GRAY  = "#8B949E"
ACCENT     = "#1F6FEB"


# ─────────────────────────────────────────────────
#  ROOT FINDING ALGORITHMS
# ─────────────────────────────────────────────────

def parse_equation(expr_str):
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    f   = sp.lambdify(x, expr, 'numpy')
    df  = sp.lambdify(x, sp.diff(expr, x), 'numpy')
    return f, df, expr

def bisection_method(f, a, b, tol=1e-6, max_iter=100):
    history = []
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs!\nCheck your interval [a, b].")
    for i in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fa, fc = f(a), f(c)
        err = abs(b - a) / 2.0
        history.append({"iter": i, "a": a, "b": b, "c": c, "f(c)": fc, "error": err})
        if err < tol or fc == 0:
            break
        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, history

def newton_raphson_method(f, df, x0, tol=1e-6, max_iter=100):
    history = []
    x = x0
    for i in range(1, max_iter + 1):
        fx  = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-12:
            raise ValueError("Derivative is zero — Newton-Raphson failed!\nTry a different starting point.")
        x_new = x - fx / dfx
        err   = abs(x_new - x)
        history.append({"iter": i, "x": x, "f(x)": fx, "f'(x)": dfx, "x_new": x_new, "error": err})
        x = x_new
        if err < tol:
            break
    return x, history

def secant_method(f, x0, x1, tol=1e-6, max_iter=100):
    history = []
    for i in range(1, max_iter + 1):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-12:
            raise ValueError("Division by zero in Secant method!\nTry different starting points.")
        x2  = x1 - f1 * (x1 - x0) / (f1 - f0)
        err = abs(x2 - x1)
        history.append({"iter": i, "x0": x0, "x1": x1, "x2": x2, "f(x2)": f(x2), "error": err})
        x0, x1 = x1, x2
        if err < tol:
            break
    return x2, history

def regula_falsi_method(f, a, b, tol=1e-6, max_iter=100):
    history = []
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs!\nCheck your interval [a, b].")
    for i in range(1, max_iter + 1):
        fa, fb = f(a), f(b)
        c  = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        err = abs(fc)
        history.append({"iter": i, "a": a, "b": b, "c": c, "f(c)": fc, "error": err})
        if err < tol:
            break
        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, history


# ─────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────

class RootFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("◈  Root Finding Calculator")
        self.root.geometry("1280x820")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        self._build_ui()

    # ── UI BUILDER ────────────────────────────────
    def _build_ui(self):
        # ── HEADER ──
        hdr = tk.Frame(self.root, bg=BG_CARD, height=56)
        hdr.pack(fill="x", padx=0, pady=0)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="◈  ROOT FINDING CALCULATOR",
                 font=("Courier New", 15, "bold"),
                 fg=BLUE, bg=BG_CARD).pack(side="left", padx=20, pady=12)
        tk.Label(hdr, text="Bisection  ·  Newton-Raphson  ·  Secant  ·  Regula Falsi",
                 font=("Courier New", 9), fg=TEXT_GRAY, bg=BG_CARD).pack(side="left", padx=5)

        # ── MAIN BODY ──
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # Left Panel
        left = tk.Frame(body, bg=BG_DARK, width=310)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_input_panel(left)

        # Right Panel
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        self._build_output_panel(right)

    # ── INPUT PANEL ───────────────────────────────
    def _build_input_panel(self, parent):
        # ── Equation Input Card ──
        self._card(parent, "EQUATION").pack(fill="x", pady=(0, 8))
        eq_card = self._last_card

        tk.Label(eq_card, text="Enter equation f(x) = 0 :",
                 font=("Courier New", 8), fg=TEXT_GRAY, bg=BG_CARD).pack(anchor="w", padx=12, pady=(8, 2))
        self.eq_var = tk.StringVar(value="x**3 - x - 2")
        eq_entry = tk.Entry(eq_card, textvariable=self.eq_var,
                            font=("Courier New", 11, "bold"),
                            bg=BG_INPUT, fg=GREEN, insertbackground=GREEN,
                            relief="flat", bd=6)
        eq_entry.pack(fill="x", padx=12, pady=(0, 8))

        # Quick equations
        tk.Label(eq_card, text="Quick Examples:", font=("Courier New", 8),
                 fg=TEXT_GRAY, bg=BG_CARD).pack(anchor="w", padx=12)
        examples = [
            ("x³-x-2",    "x**3 - x - 2"),
            ("cos(x)-x",  "cos(x) - x"),
            ("e^x - 3x",  "exp(x) - 3*x"),
            ("x²-4",      "x**2 - 4"),
        ]
        ef = tk.Frame(eq_card, bg=BG_CARD)
        ef.pack(fill="x", padx=12, pady=(2, 10))
        for i, (label, eq) in enumerate(examples):
            btn = tk.Button(ef, text=label,
                            font=("Courier New", 8), fg=BLUE, bg=BG_INPUT,
                            activebackground=ACCENT, activeforeground="white",
                            relief="flat", bd=0, cursor="hand2", padx=6, pady=3,
                            command=lambda e=eq: self.eq_var.set(e))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
        ef.columnconfigure(0, weight=1)
        ef.columnconfigure(1, weight=1)

        # ── Method Card ──
        self._card(parent, "METHOD").pack(fill="x", pady=(0, 8))
        m_card = self._last_card

        self.method_var = tk.StringVar(value="Bisection")
        methods = ["Bisection", "Newton-Raphson", "Secant", "Regula Falsi", "Compare All"]
        method_colors = [BLUE, GREEN, YELLOW, ORANGE, PURPLE]
        for m, c in zip(methods, method_colors):
            rb = tk.Radiobutton(m_card, text=f"  {m}",
                                variable=self.method_var, value=m,
                                font=("Courier New", 10),
                                fg=c, bg=BG_CARD,
                                selectcolor=BG_INPUT,
                                activebackground=BG_CARD,
                                activeforeground=c,
                                command=self._update_param_visibility)
            rb.pack(anchor="w", padx=12, pady=2)
        tk.Frame(m_card, height=8, bg=BG_CARD).pack()

        # ── Parameters Card ──
        self._card(parent, "PARAMETERS").pack(fill="x", pady=(0, 8))
        p_card = self._last_card

        self.param_frames = {}
        # Bisection / Regula Falsi params (a, b)
        f_ab = tk.Frame(p_card, bg=BG_CARD)
        self.param_frames["ab"] = f_ab
        self._param_row(f_ab, "Interval  a =", "a_var", "-2")
        self._param_row(f_ab, "Interval  b =", "b_var", "3")

        # Newton-Raphson params (x0)
        f_nr = tk.Frame(p_card, bg=BG_CARD)
        self.param_frames["nr"] = f_nr
        self._param_row(f_nr, "Start  x₀ =", "x0_var", "1.5")

        # Secant params (x0, x1)
        f_sc = tk.Frame(p_card, bg=BG_CARD)
        self.param_frames["sc"] = f_sc
        self._param_row(f_sc, "Start  x₀ =", "sc_x0_var", "1")
        self._param_row(f_sc, "Start  x₁ =", "sc_x1_var", "2")

        # Common params
        f_common = tk.Frame(p_card, bg=BG_CARD)
        f_common.pack(fill="x", padx=12, pady=(8, 4))
        self._param_row(f_common, "Tolerance =", "tol_var",   "1e-6")
        self._param_row(f_common, "Max Iter  =", "maxit_var", "100")

        self._update_param_visibility()

        # ── SOLVE BUTTON ──
        solve_btn = tk.Button(parent, text="▶  SOLVE",
                              font=("Courier New", 13, "bold"),
                              fg="white", bg=ACCENT,
                              activebackground="#388BFD",
                              activeforeground="white",
                              relief="flat", bd=0,
                              cursor="hand2", pady=10,
                              command=self._solve)
        solve_btn.pack(fill="x", pady=(4, 4))

        clear_btn = tk.Button(parent, text="✕  CLEAR",
                              font=("Courier New", 10),
                              fg=TEXT_GRAY, bg=BG_INPUT,
                              activebackground=BORDER,
                              activeforeground=TEXT_WHITE,
                              relief="flat", bd=0,
                              cursor="hand2", pady=6,
                              command=self._clear)
        clear_btn.pack(fill="x", pady=(0, 8))

        # ── Result Box ──
        self._card(parent, "RESULT").pack(fill="x", pady=(0, 4))
        r_card = self._last_card
        self.result_label = tk.Label(r_card,
                                     text="No solution yet...",
                                     font=("Courier New", 10),
                                     fg=TEXT_GRAY, bg=BG_CARD,
                                     justify="left", wraplength=270)
        self.result_label.pack(anchor="w", padx=12, pady=10)

    # ── OUTPUT PANEL ──────────────────────────────
    def _build_output_panel(self, parent):
        # Notebook tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TNotebook",
                        background=BG_DARK, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                        background=BG_CARD, foreground=TEXT_GRAY,
                        font=("Courier New", 9, "bold"),
                        padding=[14, 6])
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", BG_INPUT)],
                  foreground=[("selected", BLUE)])

        self.notebook = ttk.Notebook(parent, style="Dark.TNotebook")
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Function Graph
        self.graph_tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.graph_tab, text="  📈 Function Graph  ")
        self._build_graph_tab()

        # Tab 2: Iteration Table
        self.table_tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.table_tab, text="  📋 Iteration Table  ")
        self._build_table_tab()

        # Tab 3: Convergence Graph
        self.conv_tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.conv_tab, text="  📉 Convergence  ")
        self._build_conv_tab()

        # Tab 4: Compare All
        self.cmp_tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.cmp_tab, text="  ⚖ Compare All  ")
        self._build_cmp_tab()

    def _build_graph_tab(self):
        self.fig1 = Figure(figsize=(7, 5), facecolor=BG_CARD)
        self.ax1  = self.fig1.add_subplot(111)
        self._style_ax(self.ax1)
        self.ax1.set_title("Enter equation and press SOLVE",
                            color=TEXT_GRAY, fontsize=10, fontfamily="monospace")
        self.canvas1 = FigureCanvasTkAgg(self.fig1, self.graph_tab)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas1.draw()

    def _build_table_tab(self):
        frame = tk.Frame(self.table_tab, bg=BG_DARK)
        frame.pack(fill="both", expand=True, padx=6, pady=6)

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=BG_CARD, foreground=TEXT_WHITE,
                        fieldbackground=BG_CARD, rowheight=26,
                        font=("Courier New", 9))
        style.configure("Dark.Treeview.Heading",
                        background=BG_INPUT, foreground=BLUE,
                        font=("Courier New", 9, "bold"), relief="flat")
        style.map("Dark.Treeview", background=[("selected", ACCENT)])

        self.tree = ttk.Treeview(frame, style="Dark.Treeview", show="headings")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def _build_conv_tab(self):
        self.fig2 = Figure(figsize=(7, 5), facecolor=BG_CARD)
        self.ax2  = self.fig2.add_subplot(111)
        self._style_ax(self.ax2)
        self.ax2.set_title("Convergence plot will appear after solving",
                            color=TEXT_GRAY, fontsize=10, fontfamily="monospace")
        self.canvas2 = FigureCanvasTkAgg(self.fig2, self.conv_tab)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas2.draw()

    def _build_cmp_tab(self):
        self.fig3 = Figure(figsize=(8, 5), facecolor=BG_CARD)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, self.cmp_tab)
        self.canvas3.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas3.draw()

    # ── SOLVE LOGIC ───────────────────────────────
    def _solve(self):
        try:
            expr_str = self.eq_var.get().strip()
            if not expr_str:
                messagebox.showerror("Input Error", "Please enter an equation!")
                return

            f, df, expr = parse_equation(expr_str)
            tol    = float(self.tol_var.get())
            max_it = int(self.maxit_var.get())
            method = self.method_var.get()

            results = {}

            if method in ("Bisection", "Regula Falsi", "Compare All"):
                a = float(self.a_var.get())
                b = float(self.b_var.get())

            if method in ("Newton-Raphson", "Compare All"):
                x0 = float(self.x0_var.get())

            if method in ("Secant", "Compare All"):
                sc_x0 = float(self.sc_x0_var.get())
                sc_x1 = float(self.sc_x1_var.get())

            # Run selected method(s)
            if method == "Bisection":
                root, hist = bisection_method(f, a, b, tol, max_it)
                results["Bisection"] = (root, hist)
            elif method == "Newton-Raphson":
                root, hist = newton_raphson_method(f, df, x0, tol, max_it)
                results["Newton-Raphson"] = (root, hist)
            elif method == "Secant":
                root, hist = secant_method(f, sc_x0, sc_x1, tol, max_it)
                results["Secant"] = (root, hist)
            elif method == "Regula Falsi":
                root, hist = regula_falsi_method(f, a, b, tol, max_it)
                results["Regula Falsi"] = (root, hist)
            elif method == "Compare All":
                try:
                    r, h = bisection_method(f, a, b, tol, max_it)
                    results["Bisection"] = (r, h)
                except Exception as e:
                    results["Bisection"] = (None, str(e))
                try:
                    r, h = newton_raphson_method(f, df, x0, tol, max_it)
                    results["Newton-Raphson"] = (r, h)
                except Exception as e:
                    results["Newton-Raphson"] = (None, str(e))
                try:
                    r, h = secant_method(f, sc_x0, sc_x1, tol, max_it)
                    results["Secant"] = (r, h)
                except Exception as e:
                    results["Secant"] = (None, str(e))
                try:
                    r, h = regula_falsi_method(f, a, b, tol, max_it)
                    results["Regula Falsi"] = (r, h)
                except Exception as e:
                    results["Regula Falsi"] = (None, str(e))

            # Get primary result for display
            primary_method = [k for k in results if results[k][0] is not None]
            if not primary_method:
                raise ValueError("All methods failed. Check your inputs.")

            pm    = primary_method[0]
            root  = results[pm][0]
            hist  = results[pm][1]

            # Update result label
            self._update_result(pm, root, hist, results)

            # Draw plots
            self._plot_function(f, expr_str, results, method)
            self._plot_convergence(results, method)
            self._plot_comparison(results, method)
            self._fill_table(hist, method if method != "Compare All" else pm)

            # Switch to graph tab
            self.notebook.select(0)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_result(self, method, root, hist, all_results):
        lines = []
        colors_map = {
            "Bisection":      GREEN,
            "Newton-Raphson": BLUE,
            "Secant":         YELLOW,
            "Regula Falsi":   ORANGE,
        }
        if self.method_var.get() == "Compare All":
            lines.append("━━  COMPARE ALL RESULTS  ━━\n")
            for m, (r, h) in all_results.items():
                if r is not None:
                    iters = len(h) if isinstance(h, list) else "—"
                    lines.append(f"✔ {m}\n   Root ≈ {r:.8f}\n   Iters: {iters}\n")
                else:
                    lines.append(f"✘ {m}: Failed\n")
        else:
            iters = len(hist)
            last_err = hist[-1]["error"] if hist else "—"
            lines.append(f"✔  Method  : {method}")
            lines.append(f"✔  Root    : x ≈ {root:.10f}")
            lines.append(f"✔  f(root) : {float(self.eq_var.get() and self._safe_eval(root)):.2e}")
            lines.append(f"✔  Iters   : {iters}")
            lines.append(f"✔  Error   : {last_err:.2e}")

        self.result_label.config(
            text="\n".join(lines),
            fg=colors_map.get(method, GREEN)
        )

    def _safe_eval(self, root):
        try:
            f, _, _ = parse_equation(self.eq_var.get())
            return f(root)
        except:
            return 0.0

    # ── PLOTTING ──────────────────────────────────
    def _plot_function(self, f, expr_str, results, method):
        self.ax1.clear()
        self._style_ax(self.ax1)

        # Determine plot range
        try:
            a = float(self.a_var.get()) - 1
            b = float(self.b_var.get()) + 1
        except:
            a, b = -5, 5

        x_vals = np.linspace(a, b, 800)
        try:
            y_vals = f(x_vals)
            y_vals = np.where(np.abs(y_vals) > 1e6, np.nan, y_vals)
        except:
            y_vals = np.zeros_like(x_vals)

        self.ax1.plot(x_vals, y_vals, color=BLUE, lw=2.2, label=f"f(x) = {expr_str}")
        self.ax1.axhline(0, color=BORDER, lw=1.2)
        self.ax1.axvline(0, color=BORDER, lw=0.8)

        method_colors = {
            "Bisection":      GREEN,
            "Newton-Raphson": BLUE,
            "Secant":         YELLOW,
            "Regula Falsi":   ORANGE,
        }

        for m, (root, hist) in results.items():
            if root is not None:
                col = method_colors.get(m, GREEN)
                self.ax1.axvline(root, color=col, lw=1.2, ls="--", alpha=0.6)
                self.ax1.scatter([root], [0], color=col, s=120, zorder=6,
                                 label=f"{m}: x={root:.5f}", edgecolors=BG_DARK, linewidths=1.5)

        self.ax1.set_title(f"f(x) = {expr_str}", color=TEXT_WHITE,
                           fontsize=10, fontfamily="monospace")
        self.ax1.set_xlabel("x", color=TEXT_GRAY, fontfamily="monospace")
        self.ax1.set_ylabel("f(x)", color=TEXT_GRAY, fontfamily="monospace")
        self.ax1.legend(fontsize=8, framealpha=0.15,
                        labelcolor="white", edgecolor=BORDER,
                        facecolor=BG_CARD)
        y_rng = np.nanmax(np.abs(y_vals)) if not np.all(np.isnan(y_vals)) else 10
        self.ax1.set_ylim(-y_rng * 1.2, y_rng * 1.2)
        self.canvas1.draw()

    def _plot_convergence(self, results, method):
        self.ax2.clear()
        self._style_ax(self.ax2)

        method_colors = {
            "Bisection":      GREEN,
            "Newton-Raphson": BLUE,
            "Secant":         YELLOW,
            "Regula Falsi":   ORANGE,
        }

        plotted = False
        for m, (root, hist) in results.items():
            if root is not None and isinstance(hist, list) and hist:
                errors = [h["error"] for h in hist]
                iters  = list(range(1, len(errors) + 1))
                col    = method_colors.get(m, GREEN)
                safe_err = [max(e, 1e-15) for e in errors]
                self.ax2.semilogy(iters, safe_err, color=col, lw=2,
                                  marker="o", markersize=4,
                                  label=f"{m}  ({len(iters)} iters)")
                plotted = True

        if plotted:
            self.ax2.set_title("Convergence — Error per Iteration",
                               color=TEXT_WHITE, fontsize=10, fontfamily="monospace")
            self.ax2.set_xlabel("Iteration", color=TEXT_GRAY, fontfamily="monospace")
            self.ax2.set_ylabel("Error (log scale)", color=TEXT_GRAY, fontfamily="monospace")
            self.ax2.legend(fontsize=8, framealpha=0.15,
                            labelcolor="white", edgecolor=BORDER, facecolor=BG_CARD)
        self.canvas2.draw()

    def _plot_comparison(self, results, method):
        self.fig3.clear()

        valid = {m: (r, h) for m, (r, h) in results.items()
                 if r is not None and isinstance(h, list)}
        if not valid:
            self.canvas3.draw()
            return

        method_colors = {
            "Bisection":      GREEN,
            "Newton-Raphson": BLUE,
            "Secant":         YELLOW,
            "Regula Falsi":   ORANGE,
        }

        axes = self.fig3.subplots(1, 2)
        self.fig3.patch.set_facecolor(BG_CARD)
        self.fig3.subplots_adjust(wspace=0.35)

        # Bar: iterations
        ax_a = axes[0]
        self._style_ax(ax_a)
        names  = list(valid.keys())
        iters  = [len(v[1]) for v in valid.values()]
        colors = [method_colors.get(n, GREEN) for n in names]
        bars   = ax_a.bar(names, iters, color=colors, alpha=0.85, width=0.5)
        for bar, val in zip(bars, iters):
            ax_a.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                      str(val), ha="center", color="white", fontsize=9)
        ax_a.set_title("Iterations to Converge",
                       color=TEXT_WHITE, fontsize=9, fontfamily="monospace")
        ax_a.set_ylabel("Iterations", color=TEXT_GRAY, fontfamily="monospace")
        ax_a.tick_params(axis="x", labelrotation=12, labelsize=8)

        # Bar: final error
        ax_b = axes[1]
        self._style_ax(ax_b)
        final_errs = [v[1][-1]["error"] for v in valid.values()]
        bars2 = ax_b.bar(names, final_errs, color=colors, alpha=0.85, width=0.5)
        for bar, val in zip(bars2, final_errs):
            ax_b.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                      f"{val:.1e}", ha="center", va="bottom", color="white", fontsize=8)
        ax_b.set_title("Final Error",
                       color=TEXT_WHITE, fontsize=9, fontfamily="monospace")
        ax_b.set_ylabel("Error", color=TEXT_GRAY, fontfamily="monospace")
        ax_b.tick_params(axis="x", labelrotation=12, labelsize=8)
        ax_b.set_yscale("log")

        self.canvas3.draw()

    # ── TABLE ─────────────────────────────────────
    def _fill_table(self, hist, method):
        if not hist:
            return
        self.tree.delete(*self.tree.get_children())
        cols = list(hist[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=110, anchor="center")
        for i, row in enumerate(hist):
            tag = "even" if i % 2 == 0 else "odd"
            vals = []
            for k, v in row.items():
                if isinstance(v, float):
                    vals.append(f"{v:.8f}" if abs(v) >= 0.0001 else f"{v:.4e}")
                else:
                    vals.append(str(v))
            self.tree.insert("", "end", values=vals, tags=(tag,))
        self.tree.tag_configure("even", background=BG_CARD)
        self.tree.tag_configure("odd",  background=BG_INPUT)

    # ── HELPERS ───────────────────────────────────
    def _card(self, parent, title):
        outer = tk.Frame(parent, bg=BORDER, bd=0)
        inner = tk.Frame(outer, bg=BG_CARD, bd=0)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        tk.Label(inner, text=f"  {title}",
                 font=("Courier New", 8, "bold"),
                 fg=TEXT_GRAY, bg=BG_CARD).pack(anchor="w", padx=6, pady=(6, 0))
        tk.Frame(inner, height=1, bg=BORDER).pack(fill="x", padx=8, pady=(2, 0))
        self._last_card = inner
        return outer

    def _param_row(self, parent, label, var_name, default):
        frame = tk.Frame(parent, bg=BG_CARD)
        frame.pack(fill="x", padx=12, pady=3)
        tk.Label(frame, text=label, font=("Courier New", 9),
                 fg=TEXT_GRAY, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        setattr(self, var_name, var)
        tk.Entry(frame, textvariable=var,
                 font=("Courier New", 10), bg=BG_INPUT,
                 fg=GREEN, insertbackground=GREEN,
                 relief="flat", bd=4, width=10).pack(side="left", padx=(4, 0))

    def _style_ax(self, ax):
        ax.set_facecolor(BG_CARD)
        ax.tick_params(colors=TEXT_GRAY, labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.xaxis.label.set_color(TEXT_GRAY)
        ax.yaxis.label.set_color(TEXT_GRAY)
        ax.grid(True, color=BORDER, linestyle="--", linewidth=0.6, alpha=0.6)

    def _update_param_visibility(self):
        method = self.method_var.get()
        for f in self.param_frames.values():
            f.pack_forget()
        if method in ("Bisection", "Regula Falsi"):
            self.param_frames["ab"].pack(fill="x")
        elif method == "Newton-Raphson":
            self.param_frames["nr"].pack(fill="x")
        elif method == "Secant":
            self.param_frames["sc"].pack(fill="x")
        elif method == "Compare All":
            self.param_frames["ab"].pack(fill="x")
            self.param_frames["nr"].pack(fill="x")
            self.param_frames["sc"].pack(fill="x")

    def _clear(self):
        self.eq_var.set("x**3 - x - 2")
        self.result_label.config(text="No solution yet...", fg=TEXT_GRAY)
        self.ax1.clear(); self._style_ax(self.ax1)
        self.ax1.set_title("Enter equation and press SOLVE",
                           color=TEXT_GRAY, fontsize=10, fontfamily="monospace")
        self.canvas1.draw()
        self.ax2.clear(); self._style_ax(self.ax2)
        self.canvas2.draw()
        self.fig3.clear(); self.canvas3.draw()
        self.tree.delete(*self.tree.get_children())


# ─────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = RootFinderApp(root)
    root.mainloop()

# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sympy as sp
import numpy as np
import math
from fastapi.middleware.cors import CORSMiddleware
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()

# Allow React to communicate with the Python API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────
#  1. CORE MATH FUNCTIONS (From your original code)
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
        raise ValueError("f(a) and f(b) must have opposite signs! Check your interval [a, b].")
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
            raise ValueError("Derivative is zero — Newton-Raphson failed! Try a different starting point.")
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
            raise ValueError("Division by zero in Secant method! Try different starting points.")
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
        raise ValueError("f(a) and f(b) must have opposite signs! Check your interval [a, b].")
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
#  2. API MODELS
# ─────────────────────────────────────────────────

class BaseReq(BaseModel):
    equation: str
    tol: float = 1e-6
    max_iter: int = 100

class IntervalReq(BaseReq):
    a: float
    b: float

class NewtonReq(BaseReq):
    x0: float

class SecantReq(BaseReq):
    x0: float
    x1: float

class CompareReq(BaseModel):
    equation: str
    a: float
    b: float
    x0: float
    sc_x0: float
    sc_x1: float
    tol: float = 1e-6
    max_iter: int = 100

# Helper to generate plot data
def get_plot_data(f, center, span=5):
    x_vals = np.linspace(center - span, center + span, 400)
    y_vals = f(x_vals)
    clean_y = [None if math.isnan(y) or math.isinf(y) else float(y) for y in y_vals]
    return {"x": x_vals.tolist(), "y": clean_y}

# ─────────────────────────────────────────────────
#  3. API ENDPOINTS
# ─────────────────────────────────────────────────

@app.post("/api/bisection")
def run_bisection(req: IntervalReq):
    try:
        f, df, expr = parse_equation(req.equation)
        root, hist = bisection_method(f, req.a, req.b, req.tol, req.max_iter)
        return {"root": root, "history": hist, "plot_data": get_plot_data(f, root, abs(req.b - req.a) + 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/newton")
def run_newton(req: NewtonReq):
    try:
        f, df, expr = parse_equation(req.equation)
        root, hist = newton_raphson_method(f, df, req.x0, req.tol, req.max_iter)
        return {"root": root, "history": hist, "plot_data": get_plot_data(f, root)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/secant")
def run_secant(req: SecantReq):
    try:
        f, df, expr = parse_equation(req.equation)
        root, hist = secant_method(f, req.x0, req.x1, req.tol, req.max_iter)
        return {"root": root, "history": hist, "plot_data": get_plot_data(f, root)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/regula-falsi")
def run_regula_falsi(req: IntervalReq):
    try:
        f, df, expr = parse_equation(req.equation)
        root, hist = regula_falsi_method(f, req.a, req.b, req.tol, req.max_iter)
        return {"root": root, "history": hist, "plot_data": get_plot_data(f, root, abs(req.b - req.a) + 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/compare")
def run_compare(req: CompareReq):
    try:
        f, df, expr = parse_equation(req.equation)
        results = {}

        def safe_run(name, func, *args):
            try:
                root, hist = func(*args)
                results[name] = {"success": True, "root": root, "iters": len(hist), "final_error": hist[-1]["error"]}
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}

        safe_run("Bisection", bisection_method, f, req.a, req.b, req.tol, req.max_iter)
        safe_run("Newton-Raphson", newton_raphson_method, f, df, req.x0, req.tol, req.max_iter)
        safe_run("Secant", secant_method, f, req.sc_x0, req.sc_x1, req.tol, req.max_iter)
        safe_run("Regula Falsi", regula_falsi_method, f, req.a, req.b, req.tol, req.max_iter)

        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
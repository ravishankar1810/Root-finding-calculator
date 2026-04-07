# ◈ Root Finding Calculator

A full-stack, interactive web application designed to solve nonlinear equations using classic numerical methods. This tool visualizes mathematical convergence in real-time, providing both graphical and tabular data to help understand how different algorithms approach the root of an equation.

**Interactive Visualizations:**
<img width="1406" height="786" alt="image" src="https://github.com/user-attachments/assets/7b527509-644e-4835-9d35-77e286d3fd75" />
**Multiple Algorithms Supported:**
<img width="1405" height="895" alt="image" src="https://github.com/user-attachments/assets/0b0a1990-7527-4faf-854d-e83745093ed1" />

## ✨ Features

* **Interactive Visualizations:** Native Plotly.js integration for responsive, interactive graphs displaying the function curve and the calculated root.
* **Multiple Algorithms Supported:** * Bisection Method
  * Newton-Raphson Method
  * Secant Method
  * Regula Falsi Method
* **Iteration Tracking:** Dynamic, auto-generated data tables displaying the exact mathematical steps, error margins, and variable changes per iteration.
* **Compare All Dashboard:** A side-by-side performance comparison plotting the iterations required to converge and final error margins across all methods.
* **Modern Dark UI:** Sleek, dark-themed interface built for readability and focus.

## 🛠️ Tech Stack

**Frontend**
* React 
* Vite 
* Plotly.js (Native CDN/Dist for maximum performance)
* React Router

**Backend**
* Python 3
* FastAPI
* SymPy (Mathematical parsing and derivatives)
* NumPy 
* Pydantic (Data validation)

## 🚀 Getting Started

To run this project locally, you will need two terminal windows running simultaneously (one for the Python API, one for the React UI).

### 1. Start the Backend (FastAPI)
Navigate to the `Backend` directory and install the required Python packages:
```bash
cd Backend
pip install fastapi uvicorn sympy numpy pydantic
```
Start the Uvicorn server:
```bash
python -m uvicorn main:app --reload
```

The backend will run on http://localhost:8000

### 2. Start the Frontend (React + Vite)
Open a new terminal, navigate to the frontend directory, and install the Node dependencies:
```bash
cd root-finder-ui
npm install
```
Start the Vite development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## 📁 Project Structure
```bash
Root Finding Calculator/
├── Backend/
│   └── main.py                 # FastAPI endpoints & math logic
├── root-finder-ui/             # React Frontend
│   ├── index.html              # Entry point
│   ├── src/
│   │   ├── App.jsx             # React Router setup
│   │   ├── components/
│   │   │   └── ResultGraph.jsx # Shared Plotly graph & table component
│   │   └── pages/              # Individual method views
│   │       ├── BisectionPage.jsx
│   │       ├── NewtonPage.jsx
│   │       ├── SecantPage.jsx
│   │       ├── RegulaFalsiPage.jsx
│   │       └── ComparePage.jsx
└── README.md
```
## 📝 Usage NotesInputting Equations: 
* Use standard Python math syntax.
* For example, use x**3 - x - 2 instead of x^3 - x - 2.
* Newton-Raphson: Requires an equation with a valid, non-zero derivative at the starting point $x_0$.
* Bisection / Regula Falsi: The interval $[a, b]$ must bound the root (i.e., $f(a)$ and $f(b)$ must have opposite signs).

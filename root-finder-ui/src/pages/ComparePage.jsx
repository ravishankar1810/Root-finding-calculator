import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export default function ComparePage() {
  const [inputs, setInputs] = useState({ equation: "x**3 - x - 2", a: -2, b: 3, x0: 1.5, sc_x0: 1, sc_x1: 2 });
  const [results, setResults] = useState(null);
  
  const itersRef = useRef(null);
  const errorRef = useRef(null);

  const handleChange = (e) => setInputs({ ...inputs, [e.target.name]: e.target.value });

  const handleSolve = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/compare", {
        equation: inputs.equation, a: parseFloat(inputs.a), b: parseFloat(inputs.b),
        x0: parseFloat(inputs.x0), sc_x0: parseFloat(inputs.sc_x0), sc_x1: parseFloat(inputs.sc_x1)
      });
      setResults(response.data);
    } catch (error) {
      alert("Error: " + error.response?.data?.detail);
    }
  };

  useEffect(() => {
    if (results && window.Plotly) {
      const colorMap = { "Bisection": "#3FB950", "Newton-Raphson": "#58A6FF", "Secant": "#FFD93D", "Regula Falsi": "#FFA657" };
      const names = []; const iters = []; const errors = []; const colors = [];

      Object.keys(results).forEach(method => {
        if (results[method].success) {
          names.push(method); iters.push(results[method].iters);
          errors.push(results[method].final_error); colors.push(colorMap[method]);
        }
      });

      const layoutBase = {
        paper_bgcolor: '#161B22', plot_bgcolor: '#0D1117', font: { color: '#8B949E' },
        xaxis: { gridcolor: '#30363D' }, autosize: true, margin: { l: 50, r: 20, t: 50, b: 50 }
      };

      // Draw Iterations Chart
      window.Plotly.newPlot(itersRef.current, [{
        x: names, y: iters, type: 'bar', marker: { color: colors }, text: iters.map(String), textposition: 'auto'
      }], { ...layoutBase, title: { text: 'Iterations', font: { color: '#E6EDF3' } }, yaxis: { title: 'Iterations', gridcolor: '#30363D' } }, { responsive: true });

      // Draw Error Chart
      window.Plotly.newPlot(errorRef.current, [{
        x: names, y: errors, type: 'bar', marker: { color: colors }, text: errors.map(e => e.toExponential(1)), textposition: 'outside'
      }], { ...layoutBase, title: { text: 'Final Error', font: { color: '#E6EDF3' } }, yaxis: { type: 'log', title: 'Error (log scale)', gridcolor: '#30363D' } }, { responsive: true });
    }
  }, [results]);

  return (
    <div className="page-layout" style={{ display: 'flex', gap: '20px' }}>
      <div className="input-panel" style={{ width: '320px', background: '#161B22', padding: '20px', borderRadius: '8px' }}>
        <h3 style={{ color: '#D2A8FF', marginTop: 0 }}>⚖ Compare All</h3>
        
        <label>Equation:</label>
        <input name="equation" value={inputs.equation} onChange={handleChange} style={{ width: '100%', marginBottom: '10px' }}/>
        
        <label>Interval [a, b]:</label>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
          <input name="a" value={inputs.a} onChange={handleChange} type="number" step="0.1" />
          <input name="b" value={inputs.b} onChange={handleChange} type="number" step="0.1" />
        </div>

        <label>Newton x₀:</label>
        <input name="x0" value={inputs.x0} onChange={handleChange} type="number" step="0.1" style={{ width: '100%', marginBottom: '10px' }} />

        <label>Secant x₀, x₁:</label>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <input name="sc_x0" value={inputs.sc_x0} onChange={handleChange} type="number" step="0.1" />
          <input name="sc_x1" value={inputs.sc_x1} onChange={handleChange} type="number" step="0.1" />
        </div>

        <button onClick={handleSolve} style={{ width: '100%', background: '#1F6FEB', color: 'white', padding: '10px', border: 'none', cursor: 'pointer', borderRadius: '4px' }}>
          RUN COMPARISON
        </button>
      </div>

      <div className="graph-panel" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {results ? (
          <div style={{ display: 'flex', gap: '20px', height: '500px' }}>
            <div ref={itersRef} style={{ flex: 1 }} />
            <div ref={errorRef} style={{ flex: 1 }} />
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', background: '#161B22', color: '#8B949E', borderRadius: '8px' }}>
            Enter parameters and press Run Comparison.
          </div>
        )}
      </div>
    </div>
  );
}
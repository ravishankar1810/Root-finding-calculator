// src/pages/NewtonPage.jsx
import { useState } from 'react';
import axios from 'axios';
import ResultGraph from '../components/ResultGraph';

export default function NewtonPage() {
  const [equation, setEquation] = useState("x**3 - x - 2");
  const [x0, setX0] = useState(1.5);
  const [result, setResult] = useState(null);

  const handleSolve = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/newton", {
        equation,
        x0: parseFloat(x0)
      });
      setResult(response.data);
    } catch (error) {
      alert("Error: " + error.response?.data?.detail);
    }
  };

  return (
    <div className="page-layout" style={{ display: 'flex', gap: '20px' }}>
      <div className="input-panel" style={{ width: '300px', background: '#161B22', padding: '20px' }}>
        <h3>Newton-Raphson</h3>
        <label>Equation:</label>
        <input value={equation} onChange={e => setEquation(e.target.value)} />
        
        <label>Start x₀:</label>
        <input value={x0} onChange={e => setX0(e.target.value)} type="number" step="0.1" />
        
        <button onClick={handleSolve} style={{ background: '#1F6FEB', color: 'white', marginTop: '15px' }}>
          SOLVE
        </button>

        {/* You can map over result.history here to build your HTML table! */}
      </div>

      <div className="graph-panel" style={{ flexGrow: 1, height: '600px' }}>
        {/* Reusing the component, passing a distinct color for Newton */}
        <ResultGraph result={result} equation={equation} methodColor="#58A6FF" />
      </div>
    </div>
  );
}
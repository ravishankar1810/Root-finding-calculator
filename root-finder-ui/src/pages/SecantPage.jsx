import { useState } from 'react';
import axios from 'axios';
import ResultGraph from '../components/ResultGraph';

export default function SecantPage() {
  const [equation, setEquation] = useState("x**3 - x - 2");
  const [x0, setX0] = useState(1);
  const [x1, setX1] = useState(2);
  const [result, setResult] = useState(null);

  const handleSolve = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/secant", {
        equation, x0: parseFloat(x0), x1: parseFloat(x1)
      });
      setResult(response.data);
    } catch (error) {
      alert("Error: " + error.response?.data?.detail);
    }
  };

  return (
    <div className="page-layout" style={{ display: 'flex', gap: '20px' }}>
      <div className="input-panel" style={{ width: '300px', background: '#161B22', padding: '20px' }}>
        <h3 style={{color: '#FFD93D'}}>Secant</h3>
        <label>Equation:</label>
        <input value={equation} onChange={e => setEquation(e.target.value)} style={{ width: '100%', marginBottom: '10px' }} />
        
        <label>Start x₀:</label>
        <input value={x0} onChange={e => setX0(e.target.value)} type="number" step="0.1" style={{ width: '100%', marginBottom: '10px' }} />
        
        <label>Start x₁:</label>
        <input value={x1} onChange={e => setX1(e.target.value)} type="number" step="0.1" style={{ width: '100%', marginBottom: '10px' }} />
        
        <button onClick={handleSolve} style={{ background: '#1F6FEB', color: 'white', marginTop: '15px', width: '100%', padding: '10px' }}>
          SOLVE
        </button>
      </div>

      <div className="graph-panel" style={{ flexGrow: 1, height: '600px' }}>
        <ResultGraph result={result} equation={equation} methodColor="#FFD93D" />
      </div>
    </div>
  );
}
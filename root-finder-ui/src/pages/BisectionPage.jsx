import { useState } from 'react';
import axios from 'axios';
import ResultGraph from '../components/ResultGraph';

export default function BisectionPage() {
  const [equation, setEquation] = useState("x**3 - x - 2");
  const [a, setA] = useState(-2);
  const [b, setB] = useState(3);
  const [result, setResult] = useState(null);

  const handleSolve = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/bisection", {
        equation, a: parseFloat(a), b: parseFloat(b)
      });
      setResult(response.data);
    } catch (error) {
      alert("Error: " + error.response?.data?.detail);
    }
  };

  return (
    <div className="page-layout" style={{ display: 'flex', gap: '20px' }}>
      <div className="input-panel" style={{ width: '300px', background: '#161B22', padding: '20px' }}>
        <h3 style={{color: '#3FB950'}}>Bisection</h3>
        <label>Equation:</label>
        <input value={equation} onChange={e => setEquation(e.target.value)} style={{ width: '100%', marginBottom: '10px' }} />
        
        <label>Interval a:</label>
        <input value={a} onChange={e => setA(e.target.value)} type="number" step="0.1" style={{ width: '100%', marginBottom: '10px' }} />
        
        <label>Interval b:</label>
        <input value={b} onChange={e => setB(e.target.value)} type="number" step="0.1" style={{ width: '100%', marginBottom: '10px' }} />
        
        <button onClick={handleSolve} style={{ background: '#1F6FEB', color: 'white', marginTop: '15px', width: '100%', padding: '10px' }}>
          SOLVE
        </button>
      </div>

      <div className="graph-panel" style={{ flexGrow: 1, height: '600px' }}>
        <ResultGraph result={result} equation={equation} methodColor="#3FB950" />
      </div>
    </div>
  );
}
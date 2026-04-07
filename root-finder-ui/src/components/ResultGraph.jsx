import React, { useEffect, useRef } from 'react';

export default function ResultGraph({ result, equation, methodColor = '#3FB950' }) {
  const graphRef = useRef(null);

  // --- 1. Graph Drawing Logic ---
  useEffect(() => {
    if (result && result.plot_data && result.plot_data.x && window.Plotly) {
      const data = [
        {
          x: result.plot_data.x,
          y: result.plot_data.y,
          type: 'scatter',
          mode: 'lines',
          line: { color: '#58A6FF', width: 2.5 },
          name: 'f(x)'
        },
        {
          x: [result.root],
          y: [0], 
          type: 'scatter',
          mode: 'markers',
          marker: { color: methodColor, size: 12, line: { color: '#0D1117', width: 2 } },
          name: 'Root'
        }
      ];

      const layout = {
        title: { text: `f(x) = ${equation}`, font: { color: '#E6EDF3', family: 'Courier New' } },
        paper_bgcolor: '#161B22',
        plot_bgcolor: '#0D1117',
        font: { color: '#8B949E' },
        xaxis: { zerolinecolor: '#30363D', gridcolor: '#30363D', title: 'x' },
        yaxis: { zerolinecolor: '#30363D', gridcolor: '#30363D', title: 'f(x)' },
        autosize: true,
        margin: { l: 50, r: 20, t: 50, b: 50 }
      };

      window.Plotly.newPlot(graphRef.current, data, layout, { responsive: true });
    }
  }, [result, equation, methodColor]);


  // --- 2. Dynamic Table Generation ---
  const renderTable = () => {
    if (!result || !result.history || result.history.length === 0) return null;

    // Automatically grab the keys from the first row to use as headers
    const headers = Object.keys(result.history[0]);

    return (
      <div style={{ marginTop: '20px', background: '#161B22', borderRadius: '8px', padding: '15px', overflowX: 'auto' }}>
        <h4 style={{ color: '#E6EDF3', marginTop: 0, fontFamily: 'Courier New', borderBottom: '1px solid #30363D', paddingBottom: '10px' }}>
          📋 Iteration History
        </h4>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'Courier New', fontSize: '14px', textAlign: 'left' }}>
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header} style={{ padding: '10px 8px', color: '#58A6FF', borderBottom: '1px solid #30363D' }}>
                  {header.toUpperCase()}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.history.map((row, idx) => (
              <tr key={idx} style={{ backgroundColor: idx % 2 === 0 ? '#0D1117' : 'transparent', borderBottom: '1px solid #30363D' }}>
                {headers.map((header) => {
                  const val = row[header];
                  // Format long decimals to fit nicely in the table, just like your Tkinter code did
                  let displayVal = val;
                  if (typeof val === 'number') {
                    displayVal = (Math.abs(val) < 0.0001 && val !== 0) ? val.toExponential(4) : val.toFixed(6);
                  }
                  return (
                    <td key={header + idx} style={{ padding: '10px 8px', color: '#8B949E' }}>
                      {displayVal}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };


  // --- 3. Render States ---
  if (!result) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#8B949E', backgroundColor: '#161B22', borderRadius: '8px' }}>
        Enter parameters and press SOLVE.
      </div>
    );
  }

  if (result.error || result.success === false) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#FF6B6B', backgroundColor: '#161B22', borderRadius: '8px', padding: '20px', textAlign: 'center' }}>
        Calculation Failed:<br/>{result.error || "Unknown Error"}
      </div>
    );
  }

  if (!result.plot_data || !result.plot_data.x) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#FFA657', backgroundColor: '#161B22', borderRadius: '8px' }}>
        Result found, but graph data is missing.
      </div>
    );
  }

  // Render both the Graph and the Table below it
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Graph Container */}
      <div ref={graphRef} style={{ width: '100%', minHeight: '450px', borderRadius: '8px', overflow: 'hidden' }} />
      
      {/* Data Table */}
      {renderTable()}
    </div>
  );
}
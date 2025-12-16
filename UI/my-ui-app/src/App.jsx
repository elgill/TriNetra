import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


const MOCK_ANOMALIES = [
  { id: 1, data: "Transaction: $4,500", reason: "Exceeds average daily spend by 400%", status: "pending" },
  { id: 2, data: "Login: Stockholm, SE", reason: "IP address mismatch with known user locations", status: "pending" },
  { id: 3, data: "System: CPU Spike 98%", reason: "Unusual process 'xk82_miner' detected", status: "pending" },
];

function App() {
  const [anomalies, setAnomalies] = useState(MOCK_ANOMALIES);
  const [rejectingId, setRejectingId] = useState(null);
  const [rejectReason, setRejectReason] = useState("");

  const handleAccept = (id) => {
    setAnomalies(anomalies.filter(a => a.id !== id));
    alert(`Anomaly ${id} accepted and logged.`);
  };

  const startReject = (id) => {
    setRejectingId(id);
    setRejectReason("");
  };

  const submitReject = (id) => {
    if (!rejectReason) return alert("Please provide a reason for rejection.");
    setAnomalies(anomalies.filter(a => a.id !== id));
    console.log(`Anomaly ${id} rejected. Reason: ${rejectReason}`);
    setRejectingId(null);
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', backgroundColor: '#f4f7f6', minHeight: '100vh' }}>
      <h1>Anomalies Dashboard</h1>
      <p>Review and action detected system irregularities.</p>

      <div style={{ display: 'grid', gap: '20px' }}>
        {anomalies.length === 0 && <p>No pending anomalies to review!</p>}
        
        {anomalies.map((anomaly) => (
          <div key={anomaly.id} style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', backgroundColor: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0 }}>Anomaly ID: #{anomaly.id}</h3>
            <p><strong>Data:</strong> {anomaly.data}</p>
            <p><strong>Reason:</strong> <span style={{ color: '#d9534f' }}>{anomaly.reason}</span></p>

            {rejectingId === anomaly.id ? (
              <div style={{ marginTop: '15px', backgroundColor: '#fff5f5', padding: '15px', borderRadius: '5px' }}>
                <label>Reason for rejection:</label>
                <textarea 
                  style={{ width: '100%', display: 'block', marginTop: '8px', padding: '10px' }}
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="e.g. Known maintenance window"
                />
                <button onClick={() => submitReject(anomaly.id)} style={{ marginTop: '10px', backgroundColor: '#d9534f', color: 'white', border: 'none', padding: '8px 15px', borderRadius: '4px', cursor: 'pointer' }}>Submit Rejection</button>
                <button onClick={() => setRejectingId(null)} style={{ marginLeft: '10px', background: 'none', border: 'none', textDecoration: 'underline', cursor: 'pointer' }}>Cancel</button>
              </div>
            ) : (
              <div style={{ marginTop: '15px' }}>
                <button onClick={() => handleAccept(anomaly.id)} style={{ backgroundColor: '#5cb85c', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '4px', cursor: 'pointer', marginRight: '10px' }}>Accept Anomaly</button>
                <button onClick={() => startReject(anomaly.id)} style={{ backgroundColor: 'white', color: '#d9534f', border: '1px solid #d9534f', padding: '10px 20px', borderRadius: '4px', cursor: 'pointer' }}>Reject</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
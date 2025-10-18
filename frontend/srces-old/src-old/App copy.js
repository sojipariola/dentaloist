import React, {useState} from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);
  const [patients, setPatients] = useState([]);

  const login = async () => {
    const res = await axios.post(`${API_BASE}/auth/login`, { email, password });
    setToken(res.data.access_token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`;
    loadPatients();
  };

  const loadPatients = async () => {
    const res = await axios.get(`${API_BASE}/patients`);
    setPatients(res.data);
  };

  const createCheckout = async () => {
    const res = await axios.post(`${API_BASE}/billing/create-checkout-session`);
    window.open(res.data.checkout_url, '_blank');
  };

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h2>Digital Dentistry – Admin Demo</h2>
      {!token && (
        <div>
          <input placeholder='email' value={email} onChange={e=>setEmail(e.target.value)} />
          <input placeholder='password' type='password' value={password} onChange={e=>setPassword(e.target.value)} />
          <button onClick={login}>Login</button>
        </div>
      )}
      {token && (
        <div>
          <button onClick={loadPatients}>Load Patients</button>
          <button onClick={createCheckout}>Subscribe (Stripe)</button>
          <ul>
            {patients.map(p=> (<li key={p.id}>{p.first_name} {p.last_name}</li>))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

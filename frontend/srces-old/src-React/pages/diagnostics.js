import { useEffect, useState } from "react";
import axios from "axios";

export default function Diagnostics() {
  const [status, setStatus] = useState({
    apiReachable: "⏳ Checking...",
    loginEndpoint: "⏳ Checking...",
    dbConnected: "⏳ Checking...",
    cors: "⏳ Checking...",
    error: null,
  });

  useEffect(() => {
    const runDiagnostics = async () => {
      try {
        const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

        // 1. API Reachability
        let apiReachable;
        try {
          const apiRes = await axios.get(`${API_BASE}/health`);
          apiReachable = apiRes.status === 200 ? "✅ API reachable" : "❌ API error";
        } catch (err) {
          apiReachable = `❌ API unreachable (${err.message})`;
        }

        // 2. Login Endpoint Test
        let loginStatus;
        try {
          await axios.post(`${API_BASE}/api/auth/login`, {
            email: "test@test.com",
            password: "wrongpass",
          });
          loginStatus = "⚠️ Unexpected success (auth issue?)";
        } catch (err) {
          loginStatus = err.response
            ? `✅ Responded with ${err.response.status}`
            : `❌ No response (${err.message})`;
        }

        // 3. DB Check
        let dbConnected;
        try {
          const dbRes = await axios.get(`${API_BASE}/db-check`);
          dbConnected = dbRes.data.connected ? "✅ DB Connected" : "❌ DB Not Connected";
        } catch (err) {
          dbConnected = `❌ DB check failed (${err.message})`;
        }

        // 4. CORS Check
        let corsStatus = "❌ CORS header missing";
        try {
          const corsRes = await axios.get(`${API_BASE}/health`);
          corsStatus = corsRes.headers["access-control-allow-origin"]
            ? "✅ CORS OK"
            : "❌ CORS Missing";
        } catch {
          corsStatus = "❌ CORS check failed";
        }

        setStatus({
          apiReachable,
          loginEndpoint: loginStatus,
          dbConnected,
          cors: corsStatus,
          error: null,
        });
      } catch (err) {
        setStatus({
          apiReachable: "❌ Failed",
          loginEndpoint: "❌ Failed",
          dbConnected: "❌ Failed",
          cors: "❌ Failed",
          error: err.message,
        });
      }
    };

    runDiagnostics();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>🛠️ Dentaloist Frontend Diagnostics</h1>
      <ul>
        <li><strong>API Reachability:</strong> {status.apiReachable}</li>
        <li><strong>Login Endpoint:</strong> {status.loginEndpoint}</li>
        <li><strong>Database Connection:</strong> {status.dbConnected}</li>
        <li><strong>CORS Check:</strong> {status.cors}</li>
      </ul>
      {status.error && (
        <p style={{ color: "red" }}>⚠️ Error: {status.error}</p>
      )}
      <h2>🌍 Frontend Env Vars</h2>
      <pre>
        {JSON.stringify(
          {
            NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000",
            NODE_ENV: process.env.NODE_ENV,
          },
          null,
          2
        )}
      </pre>
    </div>
  );
}

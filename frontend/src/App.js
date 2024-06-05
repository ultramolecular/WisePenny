import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import axios from 'axios';
import config from './config';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkAuthStatus = async () => {
    try {
      const reponse = await axios.get(`${config.apiUrl}/check_auth`, { withCredentials: true });
      setAuthenticated(reponse.data.authenticated);
    } catch (error) {
      setAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={authenticated ? <Navigate to="/dashboard" /> : <Login checkAuthStatus={checkAuthStatus}/>} />
          <Route path="/dashboard" element={authenticated ? <Dashboard checkAuthStatus={checkAuthStatus}/> : <Navigate to="/login" />} />
          <Route path="/" element={authenticated ? <Navigate to="/dashboard" /> : <Login checkAuthStatus={checkAuthStatus}/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

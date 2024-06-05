import React from 'react';
import { useNavigate } from 'react-router-dom';
import { auth, provider, signInWithPopup } from '../firebaseConfig';
import config from '../config'
import axios from 'axios';

function Login({ checkAuthStatus }) {
  const nav = useNavigate();

  const googleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();
      await axios.post(`${config.apiUrl}/login`, { idToken }, { withCredentials: true });
      await checkAuthStatus();
      nav('/dashboard');
    } catch (error) {
      console.error("Error logging in with Google!", error);
    }
  };

  return (
    <div>
      <h1>Login to WisePenny</h1>
      <button onClick={googleLogin}>Login with Google</button>
    </div>
  );
}

export default Login;

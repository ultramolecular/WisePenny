import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';
import { useNavigate} from 'react-router-dom';

function AddFunds() {
  const nav = useNavigate();
  const [formData, setFormData] = useState({
    amount: '',
    method: ''
  });
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSuccessMsg('');
    setErrorMsg('');
    axios.post(`${config.apiUrl}/add_funds`, formData, { withCredentials: true })
    .then(response => {
      setSuccessMsg(`$${formData.amount} added successfully!`);
      nav('/dashboard');
    })
    .catch(error => {
      if (error.response && error.response.data && error.response.data.message) {
        setErrorMsg(error.response.data.message);
      } else {
        setErrorMsg("There was an error adding the funds!");
      }
      console.error("There was an error adding the funds!", error);
    });
  };

  return (
    <div>
      <h1>Add Funds</h1>
      {successMsg && <p style={{ color: 'green' }}>{successMsg}</p>}
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Amount:
          <input type="number" name="amount" value={formData.amount} onChange={handleChange} required />
        </label>
        <label>
          Method:
          <input type="text" name="method" value={formData.method} onChange={handleChange} required />
        </label>
        <button type="submit">Add Funds</button>
      </form>
    </div>
  );
}

export default AddFunds;

import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';
import { useNavigate } from 'react-router-dom';

function AddExpense({ fetchExpenses, fetchBalance }) {
  const nav = useNavigate();
  const [formData, setFormData] = useState({
    date: '',
    descr: '',
    amount: '',
    method: '',
    category: '',
    type: ''
  });
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrorMsg('');
    axios.post(`${config.apiUrl}/add_expense`, formData, { withCredentials: true })
    .then(response => {
      setSuccessMsg('Expense logged!');
      fetchExpenses();
      fetchBalance();
      nav('/dashboard');
    })
    .catch(error => {
      if (error.response && error.response.data && error.response.data.message) {
        setErrorMsg(error.response.data.message);
      } else {
        setErrorMsg("There was an error adding the expense!")
      }
      console.error("There was an error adding the expense!", error);
    });
  };

  return (
    <div>
      <h1>Add Expense</h1>
      {successMsg && <p style={{ color: 'green' }}>{successMsg}</p>}  {/* Display success message */}
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Date:
          <input type="date" name="date" value={formData.date} onChange={handleChange} required />
        </label>
        <label>
          Description:
          <input type="text" name="descr" value={formData.descr} onChange={handleChange} required />
        </label>
        <label>
          Amount:
          <input type="number" name="amount" value={formData.amount} onChange={handleChange} required />
        </label>
        <label>
          Method:
          <input type="text" name="method" value={formData.method} onChange={handleChange} required />
        </label>
        <label>
          Category:
          <input type="text" name="category" value={formData.category} onChange={handleChange} required />
        </label>
        <label>
          Type:
          <input type="text" name="type" value={formData.type} onChange={handleChange} required />
        </label>
        <button type="submit">Add Expense</button>
      </form>
    </div>
  );
}

export default AddExpense;

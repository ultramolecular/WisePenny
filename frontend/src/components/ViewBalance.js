import React from 'react';
import axios from 'axios';
import config from '../config';

function ViewBalance({ balance, fetchBalance }) {
  const handleClearBalance = () => {
    axios.post(`${config.apiUrl}/clear_balance`, {}, { withCredentials: true })
    .then(response => {
      fetchBalance();
    })
    .catch(error => {
      console.error("There was an error clearing the balance!", error);
    })
  }

  return (
    <div>
      <h1>Your Balance</h1>
      <p>Cash Balance: ${balance.cash_balance}</p>
      <p>Checking Balance: ${balance.checking_balance}</p>
      <p>Total Balance: ${balance.total_balance}</p>
      <button onClick={handleClearBalance}>Clear Balance</button>
    </div>
  );
}

export default ViewBalance;

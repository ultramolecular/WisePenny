import React, { useState, useEffect } from 'react';
import config from '../config';
import axios from 'axios';

function ViewBalance() {
  const [balance, setBalance] = useState({
    cash_balance: 0,
    checking_balance: 0,
    total_balance: 0
  });

  useEffect(() => {
    axios.get(`${config.apiUrl}/get_balance`, { withCredentials: true })
      .then(response => {
        setBalance(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the balance!", error);
      });
  }, []);

  return (
    <div>
      <h1>Your Balance</h1>
      <p>Cash Balance: ${balance.cash_balance}</p>
      <p>Checking Balance: ${balance.checking_balance}</p>
      <p>Total Balance: ${balance.total_balance}</p>
    </div>
  );
}

export default ViewBalance;

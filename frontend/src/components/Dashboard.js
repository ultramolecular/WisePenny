import React, { useState, useEffect } from 'react';
import config from '../config';
import axios from 'axios';
import AddExpense from './AddExpense';
import AddFunds from './AddFunds';
import ViewBalance from './ViewBalance';

function Dashboard() {
  const [expenses, setExpenses] = useState([]);
  const [editingExpense, setEditingExpense] = useState(null);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = () => {
    axios.get(`${config.apiUrl}/view_expenses`, { withCredentials: true })
    .then(response => {
      setExpenses(response.data);
    })
    .catch(error => {
      console.error("There was an error fetching the expenses!", error);
    });
  };

  const handleEditChange = (e) => {
    setEditingExpense({
      ...editingExpense,
      [e.target.name]: e.target.value
    });
  };

  const handleEditSubmit = (e) => {
    e.preventDefault();
    axios.post(`${config.apiUrl}/edit_expense/${editingExpense.id}`, editingExpense, { withCredentials: true })
    .then(response => {
      fetchExpenses();
      setEditingExpense(null);
    })
    .catch(error => {
      console.error("There was an error editing the expense!", error);
    });
  };

  const handleDelete = (id) => {
    axios.post(`${config.apiUrl}/remove_expense/${id}`, {}, { withCredentials: true })
    .then(response => {
      fetchExpenses();
    })
    .catch(error => {
      console.error("There was an error deleting the expense!", error);
    });
  };

  const startEditing = (expense) => {
    setEditingExpense(expense);
  };

  return (
    <div>
      <h1>WisePenny</h1>

      {expenses.length === 0 ? (
        <p>You have no expenses logged yet, start adding expenses to see them here!</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Amount</th>
              <th>Method</th>
              <th>Category</th>
              <th>Type</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map(expense => (
              <tr key={expense.id}>
                <td>{expense.date}</td>
                <td>{expense.descr}</td>
                <td>{expense.amount}</td>
                <td>{expense.method}</td>
                <td>{expense.category}</td>
                <td>{expense.type}</td>
                <td>
                  <button onClick={() => startEditing(expense)}>Edit</button>
                  <button onClick={() => handleDelete(expense.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

    {editingExpense && (
      <form onSubmit={handleEditSubmit}>
        <h2>Edit Expense</h2>
        <label>
          Date:
          <input type="date" name="date" value={editingExpense.date} onChange={handleEditChange} required />
        </label>
        <label>
          Description:
          <input type="text" name="descr" value={editingExpense.descr} onChange={handleEditChange} required />
        </label>
        <label>
          Amount:
          <input type="number" name="amount" value={editingExpense.amount} onChange={handleEditChange} required />
        </label>
        <label>
          Method:
          <input type="text" name="method" value={editingExpense.method} onChange={handleEditChange} required />
        </label>
        <label>
          Category:
          <input type="text" name="category" value={editingExpense.category} onChange={handleEditChange} required />
        </label>
        <label>
          Type:
          <input type="text" name="type" value={editingExpense.type} onChange={handleEditChange} required />
        </label>
        <button type="submit">Save Changes</button>
        <button onClick={() => setEditingExpense(null)}>Cancel</button>
      </form>
    )}

    <AddExpense fetchExpenses={fetchExpenses}/>
    <AddFunds />
    <ViewBalance />
    </div>
  );
}

export default Dashboard;

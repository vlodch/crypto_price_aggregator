// CurrencyPairs.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CurrencyPairs = () => {
  const [currencyPairs, setCurrencyPairs] = useState([]);

  useEffect(() => {
    const fetchCurrencyPairs = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/currency_pairs/');
        setCurrencyPairs(response.data);
      } catch (error) {
        console.error('Error fetching currency pairs:', error);
      }
    };

    fetchCurrencyPairs();
  }, []);

  return (
    <div>
      <h2>Currency Pairs</h2>
      <ul>
        {Object.entries(currencyPairs).map(([currency, rate]) => (
          <li key={currency}>
            <strong>{currency}</strong>: {rate}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CurrencyPairs;

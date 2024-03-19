// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function App() {
//   const [usdtPairs, setUsdtPairs] = useState([]);
//   const [otherPairs, setOtherPairs] = useState([]);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchCurrencyPairs = async () => {
//       try {
//         const response = await axios.get('http://localhost:8000/api/currency_pairs/');
//         const currencyPairs = response.data.currency_pairs;
        
//         // Filter currency pairs based on currency code
//         const usdtPairs = currencyPairs.filter(pair => pair.currency === 'USDT');
//         const otherPairs = currencyPairs.filter(pair => pair.currency !== 'USDT');

//         setUsdtPairs(usdtPairs);
//         setOtherPairs(otherPairs);
//       } catch (error) {
//         setError(error.message);
//       }
//     };

//     fetchCurrencyPairs();
//   }, []);

//   return (
//     <div>
//       <h1>Currency Pairs</h1>
//       {error && <p>Error fetching currency pairs: {error}</p>}
//       <div style={{ display: 'flex' }}>
//         <div style={{ flex: 1 }}>
//           <h2>USDT Pairs</h2>
//           <ul>
//             {usdtPairs.map(pair => (
//               <li key={pair.currency}>{pair.currency}: {pair.rate}</li>
//             ))}
//           </ul>
//         </div>
//         <div style={{ flex: 1 }}>
//           <h2>Other Pairs</h2>
//           <ul>
//             {otherPairs.map(pair => (
//               <li key={pair.currency}>{pair.currency}: {pair.rate}</li>
//             ))}
//           </ul>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [currencyPairs, setCurrencyPairs] = useState([]);
  const [error, setError] = useState(null);

  const fetchCurrencyPairs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/currency_pairs/');
      setCurrencyPairs(response.data.currency_pairs);
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchCurrencyPairs(); // Initial fetch
    const intervalId = setInterval(fetchCurrencyPairs, 60000); // Fetch every minute

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const calculateEquivalentUSDT = (rate, usdtRate) => {
    const rateOther = parseFloat(rate);
    const rateUsdt = parseFloat(usdtRate);
    return (rateOther / rateUsdt).toFixed(8);
  };

  return (
    <div>
      <h1>Currency Pairs</h1>
      {error && <p>Error fetching currency pairs: {error}</p>}
      <div style={{ display: 'flex' }}>
        <div style={{ flex: 1 }}>
          <h2>USDT Pairs</h2>
          <ul>
            {currencyPairs.map(pair => (
              pair.currency === 'USDT' &&
              <li key={pair.currency}>USDT/{pair.currency}: {pair.rate}</li>
            ))}
          </ul>
        </div>
        <div style={{ flex: 1 }}>
          <h2>Equivalent USDT</h2>
          <ul>
            {currencyPairs.map(pair => (
              pair.currency !== 'USDT' &&
              <li key={pair.currency}>{pair.currency}: {calculateEquivalentUSDT(pair.rate, currencyPairs.find(p => p.currency === 'USDT').rate)} USDT</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;

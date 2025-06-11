import React, { useState } from 'react';
import './App.css';

function App() {
  const [optionType, setOptionType] = useState('select'); 
  const [volatilityType, setVolatilityType] = useState('select');

  return (
    <div className="App">
      <header className="header">
        <h1 className="site-title">Options Pricer</h1>
      </header>
      <div className="intro">
        <p>
          Welcome to the site! This site is a dynamic options pricer (call & put)
          that has custom volatility entries with 5 different types. You can
          customize ticker symbol, time to expiration, period of measured
          volatility, and other parameters. I hope you find it useful!
        </p>
      </div>
      <div className="userInputs">
        <select
          className="optionInput"
          value={optionType}
          onChange={(e) => setOptionType(e.target.value)}
        >
          <option value="select">Select Option Type</option>
          <option value="call">Call Option</option>
          <option value="put">Put Option</option>
        </select>
        <input className="tickerInput" type = "text" placeholder='Ticker Symbol'/>
        <input className="strikeInput" type = "text" placeholder='Strike Price'/>
        <input className="daysInput" type = "text" placeholder='Trading Days to Expiry'/>
        <select
          className="volatilityInput"
          value={volatilityType}
          onChange={(e) => setVolatilityType(e.target.value)}
          >
            <option value="select">Select Volatility Type</option>
            <option value="historical">Historical Log</option>
            <option value="parkinsons">Parkinson's</option>
            <option value="garman-klass">Garman-Klass</option>
            <option value="rogers-satchel">Rogers-Satchel</option>
            <option value="yang-zhang">Yang-Zhang</option>
          </select>
          <input className="volatilityDaysInput" type = "text" placeholder="Period of Vol. (days)"/>
      </div>
    </div>
  );
}

export default App;

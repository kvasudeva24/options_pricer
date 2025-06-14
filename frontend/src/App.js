import React, { useState } from 'react';
import './App.css';
import './index.js';

function App() {
  const [optionType, setOptionType] = useState('select'); 
  const [volatilityType, setVolatilityType] = useState('select');

//function to set the price output with animation
function setPriceOutput() {
  const volatilityMap = {
    "select": 0,
    "historical": 1,
    "parkinsons": 2,
    "garman-klass": 3,
    "rogers-satchel": 4,
    "yang-zhang": 5
  };

  const userOptionChoice = document.getElementById("optionInput").value;
  const userTicker = document.getElementById("tickerInput").value;
  const userStrike = parseFloat(document.getElementById("strikeInput").value);
  const userDays = parseInt(document.getElementById("daysInput").value);
  const userVolatilityType = volatilityMap[document.getElementById("volatilityInput").value];
  const userVolatilityDays = parseInt(document.getElementById("volatilityDaysInput").value);

  if(userOptionChoice === 'select' || !userTicker || isNaN(userDays) ||
    isNaN(userStrike) || userVolatilityType === 0 || userVolatilityDays < 2){
    alert("Please enter valid inputs");
    return;
  }

  if(userOptionChoice === 'call'){
    const data = {
    ticker: userTicker,
    option_vol: userVolatilityType,
    period_vol: userVolatilityDays,
    period_opt: userDays,
    strike: userStrike
  };

    const endpoint = 'http://localhost:8000/api/call-price';

    return fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {
      if (response.price !== undefined && response.price !== null) {
        const outputEl = document.getElementById("outputPrice");
        outputEl.innerText = "$" + response.price.toFixed(2);
        outputEl.classList.remove("green-flash");
        void outputEl.offsetWidth; 
        outputEl.classList.add("green-flash");
      } else {
        alert("Server side issue: " + response.error);
        return;
      }
    })
    .catch(error => {
      alert("Error fetching request: " + error.message);
      return;
    });
  } else {
    const data = {
    ticker: userTicker,
    option_vol: userVolatilityType,
    period_vol: userVolatilityDays,
    period_opt: userDays,
    strike: userStrike
    };

    const endpoint = 'http://localhost:8000/api/put-price';

    return fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {
      if (response.price !== undefined && response.price !== null) {
        const outputEl = document.getElementById("outputPrice");
        outputEl.innerText = "$" + response.price.toFixed(2);
        outputEl.classList.remove("green-flash");
        void outputEl.offsetWidth; 
        outputEl.classList.add("green-flash");
      } else {
        alert("Server side issue: " + response.error);
        return;
      }
    })
    .catch(error => {
      alert("Error fetching request: " + error.message);
      return;
    });
  }
}




  //actually building the site out
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
          <br/>
          <br/>
          <strong> DISCLAIMER: The dynamic heatmap generator will only return accurate reports during market hours (9:30 AM - 4:00 PM EST) as the yfinance API lists bid and ask prices for options as 0.00 during after hours.</strong> 
        </p>
      </div>
      <div className="userInputs">
        <select
          id="optionInput"      
          className="optionInput"
          value={optionType}
          onChange={(e) => setOptionType(e.target.value)}
        >
          <option value="select">Select Option Type</option>
          <option value="call">Call Option</option>
          <option value="put">Put Option</option>
        </select>
        <input id="tickerInput" className="tickerInput" type = "text" placeholder='Ticker Symbol'/>
        <input id="strikeInput" className="strikeInput" type = "number" placeholder='Strike Price'/>
        <input id="daysInput" className="daysInput" type = "number" placeholder='Trading Days to Expiry'/>
        <select
          id="volatilityInput"
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
          <input id="volatilityDaysInput"className="volatilityDaysInput" type = "number" placeholder="Period of Vol. (days)"/>
      </div>
      <div className = "buttonContainer">
        <button onClick={setPriceOutput} className="priceButton">Generate Your Option Price</button>
        <button className="heatmapButton">Generate Dynamic Heatmap</button>
      </div>
      <div className="outputContainer">
        <output className="outputPrice" id="outputPrice">$0.00</output>
        <img id="heatmapImage" alt="Heatmap" style={{ width: '100%', height: 'auto' }} />
      </div>
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import './App.css';
import './index.js';

function App() {
  const [optionType, setOptionType] = useState('select'); 
  const [volatilityType, setVolatilityType] = useState('select');


//function to calculate the option price based on user inputs
function calculateOptionPrice() {
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
    return Promise.resolve(null);
  }

  if(userOptionChoice === 'call'){
    return calculateCallOption(userTicker, userStrike, userDays, userVolatilityType, userVolatilityDays);
  } else {
    return Promise.resolve(null);  // For now
  }
}


function calculateCallOption(userTicker, userStrike, userDays, userVolatilityType, userVolatilityDays){
  const data = {
    ticker: userTicker,
    option_vol: userVolatilityType,
    period_vol: userVolatilityDays,
    period_opt: userDays,
    strike: userStrike
  };

  const endpoint = 'http://localhost:5000/api/call-price';

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
      return response.price;
    } else {
      alert("Server side issue: " + response.error);
      return null;
    }
  })
  .catch(error => {
    alert("Error fetching request: " + error.message);
    return null;
  });
}


//function to set the price output with animation
function setPriceOutput() {
  const output = document.getElementById("outputPrice");
  const rawValue = output.innerText.replace('$', '');
  const startValue = isNaN(parseFloat(rawValue)) ? 0 : parseFloat(rawValue);
  const duration = 800;
  const start = performance.now();

  calculateOptionPrice().then(finalValue => {
    if (typeof finalValue !== 'number' || isNaN(finalValue)) {
      return;
    }

    output.style.color = "#34eb46";

    function animate(time) {
      const elapsed = time - start;
      const progress = Math.min(elapsed / duration, 1);
      const currentValue = (startValue + (finalValue - startValue) * progress).toFixed(2);
      output.innerText = `$${currentValue}`;

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  });
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
      </div>
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import './App.css';
import './index.js';
import loadingGif from './l.gif';


function App() {
  const [optionType, setOptionType] = useState('select'); 
  const [volatilityType, setVolatilityType] = useState('select');

  function resetAll(){
    let heatmapOut = document.getElementById("heatmapImage");
    heatmapOut.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=";
    
    document.getElementById("tickerInput").value = "";
    document.getElementById("strikeInput").value = "";
    document.getElementById("daysInput").value = "";
    document.getElementById("volatilityDaysInput").value = "";

    document.getElementById("optionInput").value = "select";
    document.getElementById("volatilityInput").value = "select";

    document.getElementById("outputPrice").innerText = "$0.00"

    document.getElementById("outputDelta").innerText = "0.00"
    document.getElementById("outputTheta").innerText = "0.00"
    document.getElementById("outputGamma").innerText = "0.00"
    document.getElementById("outputRho").innerText = "0.00"
  }


  function setHeatmapOutput() {
    //set heatmap to loading image
    let heatmapOut = document.getElementById("heatmapImage");
    heatmapOut.src = loadingGif;

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
    const userVolatilityType = volatilityMap[document.getElementById("volatilityInput").value];
    const userVolatilityDays = parseInt(document.getElementById("volatilityDaysInput").value);

    if(userOptionChoice === 'select' || !userTicker || userVolatilityType === 0 || userVolatilityDays < 2){
      alert("Please enter valid inputs");
      return;
    }

    if(userOptionChoice === 'call'){
      const data = {
        ticker: userTicker, 
        option_vol: userVolatilityType,
        period_vol: userVolatilityDays
      };

      const endpoint = 'http://localhost:8000/api/call-heatmap'

      return fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type' : 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(response =>{
        if(response.heatmap !== undefined && response.heatmap !== null){
            let heatmapOut = document.getElementById("heatmapImage");
            heatmapOut.src = "data:image/png;base64," + response.heatmap;
        } else {
          alert("Server side issue: " + response.error);
          return;
        }
      })
      .catch(error => {
        alert("Error fecthing request: " + error.message);
        return;
      });
    } else {
      const data = {
        ticker: userTicker, 
        option_vol: userVolatilityType,
        period_vol: userVolatilityDays
      };

      const endpoint = 'http://localhost:8000/api/put-heatmap';

      return fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(response => {
        if(response.heatmap !== undefined && response.heatmap !== null){
          let heatmapOut = document.getElementById("heatmapImage");
          heatmapOut.src = "data:image/png;base64," + response.heatmap;
        } else {
          alert("Server side error: " + response.error);
          return;
        }
      })
      .catch(error => {
        alert("Error fetching request: " + error.message);
        return;
      });
    }
  }


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

  function getGreekSymbols(){
      const volatilityMap = {
      "select": 0,
      "historical": 1,
      "parkinsons": 2,
      "garman-klass": 3,
      "rogers-satchel": 4,
      "yang-zhang": 5
    };

      const optionMap = {
      "select": -1,
      "call": 0,
      "put": 1
    };

    const optionChoice = optionMap[document.getElementById("optionInput").value];
    const userTicker = document.getElementById("tickerInput").value;
    const userStrike = parseFloat(document.getElementById("strikeInput").value);
    const daysExpiry = parseInt(document.getElementById("daysInput").value);
    const volChoice = volatilityMap[document.getElementById("volatilityInput").value];
    const periodVol = parseInt(document.getElementById("volatilityDaysInput").value);
    let currOptionOut = document.getElementById("outputPrice").innerText;
    currOptionOut = currOptionOut.substring(1);
    const optionOut = parseFloat(currOptionOut);

    const data = {
      opt_type: optionChoice,
      ticker: userTicker,
      strike_price: userStrike,
      option_vol: volChoice,
      period_vol: periodVol,
      period_opt: daysExpiry,
      output: optionOut
    };

    if(optionChoice === -1 || !userTicker || volChoice === 0 || periodVol < 2 || daysExpiry === 0 || isNaN(optionOut) || isNaN(userStrike)){
      alert("Please enter valid inputs");
      return;
    }

    const endpoint = 'http://localhost:8000/api/get-greeks';

    return fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {
      let deltaOut = document.getElementById("outputDelta");
      let gammaOut = document.getElementById("outputGamma");
      let thetaOut = document.getElementById("outputTheta");
      let rhoOut = document.getElementById("outputRho");

      deltaOut.innerText = response['Delta'].toFixed(2);
      gammaOut.innerText = response['Gamma'].toFixed(2);
      thetaOut.innerText = response['Theta'].toFixed(2);
      rhoOut.innerText = response['Rho'].toFixed(2);
    })
    .catch(error => {
      alert("Error fetching request: " + error.message);
      return;
    })


  }



  //actually building the site out
  return (
    <div className="App">
      <header className="header">
        <h1 className="site-title">Pyros Options Pricer</h1>
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
          <br/>
          <br/>
          <strong> NOTE: Please wait 10-15 seconds for the heatmap to load as compressing and sending images has noticable latency</strong>
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
      </div>
      <div className="outputContainer">
        <output className="outputPrice" id="outputPrice">$0.00</output>
      </div>
      <div className="gButton">
        <button onClick={getGreekSymbols} className="greeksButton">Get Greeks</button>
      </div>
      <div className="greeksOutput">
        <output className="outputGreek" id="outputDelta">0.00</output>
        <output className="outputGreek" id="outputGamma">0.00</output>
        <output className="outputGreek" id="outputTheta">0.00</output>
        <output className="outputGreek" id="outputRho">0.00</output>
      </div>
      <div className = "greeksLabel">
        <p className="greeksID">Delta ------- Gamma ------ Theta --------- Rho</p>
      </div>
      <div className = "heatmapContainer">
        <button onClick={setHeatmapOutput} className="heatmapButton">Generate Your Dynamic Heatmap</button>
      </div>
      <div className="heatmapOutput">
        <img id="heatmapImage" className="heatMapImage" alt="Heatmap" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="/>
      </div>
        <div className = "reset">
          <footer>
            <button onClick={resetAll} className="resetButton"> Reset All</button>
          </footer>
        </div>
    </div>
  );
}

export default App;

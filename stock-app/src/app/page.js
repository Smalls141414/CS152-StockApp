"use client";

import styles from "./page.module.css";
import axios from 'axios';
import React, { useState } from 'react';

export default function Home() {
  const [retireResult, setRetireResult] = useState([]);
  const [portResult, setPortResult] = useState([]);
  const [expend, setExpend] = useState('');
  const [currentAge, setCurrentAge] = useState('');
  const [retireAge, setRetireAge] = useState('');
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [frequency, setFrequency] = useState('');
  const [investment, setInvestment] = useState('');

  // Retirement Calculator Form
  const handleRetirementCalc = async(e) => {
    e.preventDefault();

    const retireForm = {
      expend: expend,
      current_age: currentAge,
      retire_age: retireAge
    }

    // Get & Set Results
    const response = await axios.post('http://localhost:5000/retire', retireForm);
    setRetireResult(response.data);

    // Display Results
    document.getElementById("calcresult").style.display = 'block';
  }

  // Portfolio Value Estimation Form
  const handlePortfolio = async(e) => {
    e.preventDefault();

    const portForm = {
      ticker: ticker,
      start_date: startDate,
      end_date: endDate,
      investment: investment,
      frequency: frequency
    }

    // Get & Set Results
    const response = await axios.post('http://localhost:5000/portfolio', portForm);
    setPortResult(response.data);

    // Display Results
    document.getElementById("portresult").style.display = 'block';
  }

  return (
    <div className={styles.page}>
        <div className={styles.header}>
          <h1>Financial Planner - Stock App</h1>
        </div>
        <div className={styles.flexparent}>
          <div className={styles.retirementcalc}>
            <h2>Retirement Calculator</h2>
            <form onSubmit={handleRetirementCalc}>
              <p>Annual Expenditure($):</p>
              <input type="text" className={styles.textfield} value={expend} onChange={(e)=> setExpend(e.target.value)}/>
              <p>Current Age: </p>
              <input type="text" className={styles.textfield} value={currentAge} onChange={(e)=> setCurrentAge(e.target.value)}/>
              <p>Planned Retirement Age: </p>
              <input type="text" className={styles.textfield} value={retireAge} onChange={(e)=> setRetireAge(e.target.value)}/>

              <input type="submit" className={styles.tertbutton} value="Calculate"/>
            </form>
            <div className={styles.calcresult} id="calcresult"> 
              <p className={styles.resulttext}> You would need to have saved a total of ${retireResult.retire_amt} to retire comfortably {retireResult.retire_years} years from today (at the time of retirement). </p>
              <p className={styles.resulttext}> This amount is adjusted for inflation of {retireResult.inflate_rate}% based on the average annual inflation in the United States over the past {retireResult.time_period} years and reflects the future value, not the amount you need to have saved today. </p>
              <p className={styles.resulttext}> For context, the amount would be worth ${retireResult.retire_amt_raw} today. </p>
            </div>
          </div>

          <div className={styles.portfolioest}>
            <h2>Portfolio Value Estimator</h2>
            <form onSubmit={handlePortfolio}>
              <p>Ticker Symbol:</p>
              <input type="text" className={styles.textfield} value={ticker} onChange={(e)=> setTicker(e.target.value)}/>
              <p>Start Date (YYYY-MM-DD): </p>
              <input type="text" className={styles.textfield} value={startDate} onChange={(e)=> setStartDate(e.target.value)}/>
              <p>End Date (YYYY-MM-DD): </p>
              <input type="text" className={styles.textfield} value={endDate} onChange={(e)=> setEndDate(e.target.value)}/>
              <p>Frequency Daily(d), Monthly(m), or Yearly(y): </p>
              <input type="text" className={styles.textfield} value={frequency} onChange={(e)=> setFrequency(e.target.value)}/>
              <p>Investment($): </p>
              <input type="text" className={styles.textfield} value={investment} onChange={(e)=> setInvestment(e.target.value)}/>

              <input type="submit" className={styles.secbutton} value="Calculate"/>
            </form>
            <div className={styles.portfolioresult} id="portresult">
              <p className={styles.resulttext}> Your portfolio of {portResult.stocks} stocks would be valued at ${portResult.value} with a profit of ${portResult.profit}. </p>
              <p className={styles.resulttext}> For context, the average price of {portResult.ticker} during the time period was ${portResult.avg_price}, and the end price was ${portResult.end_price}. Based on daily dollar cost averaging, the absolute rate of return was {portResult.abs_return}%. </p>
              <p className={styles.resulttext}> If you held onto the stocks until today, your portfolio value would have been: ${portResult.today_value} with a net growth of ${portResult.final_profit} which is {portResult.final_return}% of total growth with an annualized rate of return of {portResult.ann_return}%.</p>
            </div>        
          </div>
        </div>
    </div>
  );
}
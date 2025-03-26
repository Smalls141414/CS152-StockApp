"use client";

import styles from "./page.module.css";
import axios from 'axios';
import React, { useState } from 'react';

export default function Home() {
  const [test, setTest] = useState('');

  const testResponse = async(e) => {
    e.preventDefault();
    const response = await axios.get('http://localhost:5000/test', test);
    setTest(response.data);
  }

  return (
    <div className={styles.page}>
        <div className={styles.header}>
          <h1>Financial Planner - Stock App</h1>
        </div>
        <div className={styles.retirementcalc}>
          <form>
            <h2>Retirement Calculator</h2>
            <p>Annual Expenditure: $</p>
            <input type="text" className={styles.textfield} />
            <p>Current Age: </p>
            <input type="text" className={styles.textfield} />
            <p>Planned Retirement Age: </p>
            <input type="text" className={styles.textfield} />

            <input type="button" onClick={testResponse} className={styles.tertbutton} value="Calculate"/>
          </form>
        </div>
        <div className={styles.portfolioest}>
          <h2>Portfolio Value Estimator</h2>
          <button onClick={testResponse} className={styles.secbutton}> Calculate </button>
        </div>
    </div>
  );
}

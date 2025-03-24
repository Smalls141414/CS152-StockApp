"use client";
import styles from "./page.module.css";
import axios from 'axios';
import React, { useEffect, useState } from 'react';

export default function Home() {
  const [test, setTest] = useState('');

  const testResponse = async(e) => {
    e.preventDefault();
    const response = await axios.get('http://localhost:5000/test', test);
    setTest(response.data);
  }

  return (
    <div className={styles.page}>
        <p> Stock {test} </p>
        <button onClick={testResponse}> test </button>
    </div>
  );
}

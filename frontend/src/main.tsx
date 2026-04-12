import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

/**
 * Entry point for the React application.
 * Initializes the root element and renders the App component within StrictMode.
 * StrictMode helps identify potential problems in an application during development.
 */
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

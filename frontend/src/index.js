import React from "react";
import ReactDOM from "react-dom/client"; // Importe o 'client' de 'react-dom'
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

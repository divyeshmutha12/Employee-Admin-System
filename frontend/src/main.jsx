import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Import Ant Design global styles once here so all components are styled.
import "antd/dist/reset.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

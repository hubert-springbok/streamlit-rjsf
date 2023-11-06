import React from "react";
import { createRoot } from "react-dom/client";
import JsonformComponent from "./App";

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <JsonformComponent />
  </React.StrictMode>
);

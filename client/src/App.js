import React from "react";
import { Route } from "react-router-dom";
import "./App.scss";
import Main from "./components/main/Main";

function App() {
  return (
    <div className="App">
      <Route exact path="/" component={Main}></Route>
    </div>
  );
}

export default App;

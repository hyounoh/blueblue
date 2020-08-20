import React from "react";
import { Route } from "react-router-dom";
import "./App.scss";
import Main from "./components/main/Main";
import Admin from "./components/admin/Admin";

function App() {
  return (
    <div className="App">
      <Route exact path="/" component={Main}></Route>
      <Route exact path="/admin" component={Admin}></Route>
    </div>
  );
}

export default App;

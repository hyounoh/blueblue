import React from "react";
import "./App.css";
import Title from "./components/Title";
import Dashboard from "./components/Dashboard";
import Wordcloud from "./components/Wordcloud";
import PetitionList from "./components/PetitionList";
import TimeGraph from "./components/TimeGraph";
import Footer from "./components/Footer";
import KeywordProvider from "./context/KeywordProvider";
import { positions, Provider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

function App() {
  const options = {
    timeout: 10000,
    position: positions.MIDDLE,
  };

  return (
    <div className="App">
      <div className="Title">
        <Provider template={AlertTemplate} {...options}>
          <Title></Title>
        </Provider>
      </div>
      <div>
        <Dashboard></Dashboard>
      </div>
      <KeywordProvider>
        <div>
          <Wordcloud></Wordcloud>
        </div>
        <div>
          <PetitionList></PetitionList>
        </div>
      </KeywordProvider>
      <div>
        <TimeGraph></TimeGraph>
      </div>
      <div className="FooterArea">
        <Footer></Footer>
      </div>
    </div>
  );
}

export default App;

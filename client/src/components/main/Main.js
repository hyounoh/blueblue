import React from "react";
import "./Main.css";

import Title from "./Title";
import Dashboard from "./Dashboard";
import Wordcloud from "./Wordcloud";
import PetitionList from "./PetitionList";
import TimeGraph from "./TimeGraph";
import Footer from "./Footer";
import KeywordProvider from "../../context/KeywordProvider";
import { positions, Provider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

const Main = () => {
  const options = {
    timeout: 10000,
    position: positions.MIDDLE,
  };

  return (
    <div className="Main">
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
};

export default Main;

import React, { useState, useEffect } from "react";
import "../../css/main/Dashboard.css";
import axios from "axios";
import config from "../../settings/config.json";

const Dashboard = () => {
  // Define state of wordcloud data
  const [words, setWords] = useState("");
  const [count, setCount] = useState(0);

  // Set event on refresh to load wordcloud data
  const onRefresh = () => {
    axios
      .get(
        "http://" +
          config.host +
          ":" +
          config.port +
          "/recentword?use_stopword=1"
      )
      .then((response) => {
        let words = response.data["results"];
        setWords(words);
      })
      .catch((response) => {
        console.log(response);
      });

    axios
      .get(
        "http://" + config.host + ":" + config.port + "/petition-graph?recent=1"
      )
      .then((response) => {
        let count = response.data["results"]["sum"];
        setCount(count);
      })
      .catch((response) => {
        console.log(response);
      });
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    console.log("Dashboard rendered!");
    onRefresh();
  }, []);

  return (
    <div className="Dashboard">
      <div className="DashboardItem Word">
        <div className="DashboardItemTitle">최근 일주일 핵심 단어</div>
        <div className="DashboardItemContent">{words}</div>
      </div>
      <div className="DashboardItem Count">
        <div className="DashboardItemTitle">최근 일주일 청원 개수</div>
        <div className="DashboardItemContent">{count} 개</div>
      </div>
    </div>
  );
};

export default Dashboard;

import React, { useEffect } from "react";
import axios from "axios";
import { useAlert } from "react-alert";
import config from "../settings/config.json";
import "../css/Title.css";

const Title = () => {
  const alert = useAlert();

  // Set event on refresh to load wordcloud data
  const onRefresh = () => {
    axios
      .get("http://" + config.host + ":" + config.port + "/status")
      .then((response) => {
        console.log(response);
      })
      .catch((response) => {
        console.log(response);
        alert.show("Please check internet connection");
      });
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    console.log("Title rendered!");
    onRefresh();
  });

  return <div className="Title">청와대 국민청원을 araboja</div>;
};

export default Title;

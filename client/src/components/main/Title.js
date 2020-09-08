import React, { useEffect } from "react";
import axios from "axios";
import { useAlert } from "react-alert";
import config from "../../settings/config.json";
import "./Title.scss";

const Title = () => {
  const alert = useAlert();

  // Set event on refresh to load wordcloud data
  const onRefresh = () => {
    axios.get("http://" + config.host + ":" + config.port + "/status").catch((response) => {
      console.log(response);
      alert.show("Please check internet connection");
    });
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    onRefresh();
  });

  return <div className="Title">청와대 국민청원을 araboja</div>;
};

export default Title;

import React, { useState, useEffect, useContext, useRef } from "react";
import "./Wordcloud.scss";
import ReactWordcloud from "react-wordcloud";
import { select } from "d3-selection";
import axios from "axios";
import config from "../../settings/config.json";
import KeywordContext from "../../context/Keyword.context";

const scrollToRef = (ref) => window.scrollTo({ top: 1000, behavior: "smooth" });

const Wordcloud = () => {
  // Define state of wordcloud data
  const [words, setWords] = useState([]);
  const { change } = useContext(KeywordContext);

  const myRef = useRef(null);
  const executeScroll = () => scrollToRef(myRef);

  // Set callback on word in wordcloud
  const getCallback = (callbackName) => (word, event) => {
    const isActive = callbackName !== "onWordMouseOut";
    const element = event.target;
    const text = select(element);
    text
      .on("click", () => {
        if (isActive) {
          // Bind Context using clicked word
          change(word.text);
          executeScroll();
        }
      })
      .attr("background", "white");
  };

  // Set event on refresh to load wordcloud data
  const onRefresh = () => {
    axios
      .get("http://" + config.host + ":" + config.port + "/word?use_stopword=1&limit=30&interval=30")
      .then((response) => {
        let words = response.data["results"];
        let words_formatted = words.map((word) => ({
          text: word["word"],
          value: word["count"],
        }));
        setWords(words_formatted);
      })
      .catch((response) => {
        console.log(response);
      });
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    onRefresh();
  }, []);

  return (
    <div className="Container">
      <div className="ContainerHeader">
        <div className="ContainerTitle">워드 클라우드 (최근 30일)</div>
      </div>

      <div className="ContainerContent">
        <ReactWordcloud
          words={words}
          options={{
            fontFamily: "NanumSquareRoundR",
            fontSizes: [40, 90],
            rotations: 1,
            rotationAngles: [0],
          }}
          callbacks={{
            onWordClick: getCallback("onWordClick"),
            onWordMouseOut: getCallback("onWordMouseOut"),
            onWordMouseOver: getCallback("onWordMouseOver"),
          }}
        />
      </div>
    </div>
  );
};

export default Wordcloud;

import React, { useState, useEffect } from 'react';
import '../css/Wordcloud.css'
import ReactWordcloud from 'react-wordcloud';
import { select } from 'd3-selection';
import RefreshIcon from '@material-ui/icons/Refresh';
import { IconButton } from '@material-ui/core';
import axios from 'axios'


const Wordcloud = () => {

    // Define state of wordcloud data
    const [words, setWords] = useState([]);

    // Set callback on word in wordcloud
    const getCallback = callbackName => (word, event) => {
        const isActive = callbackName !== 'onWordMouseOut'
        const element = event.target
        const text = select(element)
        text
            .on('click', () => {
                if (isActive) {
                    console.log(word.text);
                }
            })
            .attr('background', 'white')
    };

    // Set event on refresh to load wordcloud data
    const onRefresh = () => {
        axios.get('http://localhost:5001/wordcloud?use_stopword=1&limit=20')
            .then(
                response => {
                    let words = response.data['results']
                    let words_formatted = words.map((word) => ({ 'text': word['word'], 'value': word['count'] }))
                    console.log(words_formatted)

                    setWords(words_formatted);
                }
            )
            .catch(
                response => {
                    console.log(response)
                }
            );
    };

    // Load wordcloud when this page is rendered.
    useEffect(() => {
        console.log('rendered!');
        onRefresh();
    }, []);

    return (
        <div className="Wordcloud">
            <IconButton className="" onClick={onRefresh}>
                <RefreshIcon></RefreshIcon>
            </IconButton>
            <ReactWordcloud
                words={words}
                options={{
                    fontFamily: 'NanumSquareRoundR',
                    fontSizes: [40, 90],
                    rotations: 1,
                    rotationAngles: [0]
                }}
                callbacks={{
                    onWordClick: getCallback('onWordClick'),
                    onWordMouseOut: getCallback('onWordMouseOut'),
                    onWordMouseOver: getCallback('onWordMouseOver'),
                }}
            />
        </div>
    );
}

export default Wordcloud;
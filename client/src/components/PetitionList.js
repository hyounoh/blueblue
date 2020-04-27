import React, { useState, useEffect, useContext } from 'react';
import '../css/PetitionList.css';
import RefreshIcon from '../icons/round_refresh_black_18dp.png';
import axios from 'axios';
import KeywordContext from '../context/Keyword.context';


const PetitionList = () => {

    // Define state of wordcloud data
    const [petitions, setPetitions] = useState([]);
    const { word } = useContext(KeywordContext);

    // Set event on refresh to load wordcloud data
    const onRefresh = () => {
        axios.get('http://localhost:5001/petition-word?keyword=코로나')
            .then(
                response => {
                    let petitions = response.data['results']
                    let petitions_formatted = petitions.map((petition) => ({ 'title': petition['title'], 'url': petition['url'] }))
                    console.log(petitions_formatted)

                    setPetitions(petitions_formatted);
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
        console.log('PetitionList rendered!');
        onRefresh();
    }, []);

    return (
        <div className="PetitionListContainer">
            <div className="Refresh" onClick={onRefresh}>
                <img src={RefreshIcon} alt="Refresh"></img>
            </div>
            <div>
              {word}
            </div>
        </div>
    );
}

export default PetitionList;
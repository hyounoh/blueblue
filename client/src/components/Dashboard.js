import React, { useState, useEffect } from 'react';
import '../css/Dashboard.css';
import axios from 'axios'

const Dashboard = () => {

    // Define state of wordcloud data
    const [words, setWords] = useState('');

    // Set event on refresh to load wordcloud data
    const onRefresh = () => {
        axios.get('http://localhost:5001/recentword?use_stopword=1')
            .then(
                response => {
                    let words = response.data['results']
                    console.log(words)

                    setWords(words);
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
        <div className="Dashboard">
            <div className="DashboardItem Word">
                <div className="DashboardItemTitle">
                    최근 일주일 핵심 단어
                </div>
                <div className="DashboardItemContent">
                    {words}
                </div>
            </div>
            <div className="DashboardItem Count">
                <div className="DashboardItemTitle">
                    최근 일주일 청원 개수
                </div>
                <div className="DashboardItemContent">
                    00 개
                </div>
            </div>
        </div>
    )
}

export default Dashboard;
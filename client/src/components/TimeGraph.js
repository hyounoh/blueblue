import React, { useState, useEffect } from 'react';
import '../css/TimeGraph.css'
import '../../node_modules/react-vis/dist/style.css';
import { XYPlot, VerticalBarSeries, XAxis } from 'react-vis';
import RefreshIcon from '../icons/round_refresh_black_18dp.png';
import axios from 'axios'

const TimeGraph = () => {

    // Define state of wordcloud data
    const [graph, setGraph] = useState([{ x: 0, y: 0 }]);

    // Set event on refresh to load wordcloud data
    const onRefresh = () => {
        axios.get('http://localhost:5001/petition-graph?recent=0')
            .then(
                response => {
                    let graph = response.data['results']['graph'];
                    console.log(graph)
                    let graph_formatted = graph.map((item) => ({ 'x': item['date'], 'y': item['count'] }))
                    console.log(graph_formatted);

                    setGraph(graph_formatted);
                }
            )
            .catch(
                response => {
                    console.log(response);
                }
            );
    };

    // Load wordcloud when this page is rendered.
    useEffect(() => {
        console.log('rendered!');
        onRefresh();
    }, []);

    return (
        <div className="TimeGraph">
            <div className="Refresh" onClick={onRefresh}>
                <img src={RefreshIcon} alt="Refresh"></img>
            </div>
            <XYPlot height={500} width={1300} xType="ordinal">
                <XAxis />
                <VerticalBarSeries data={graph} />
            </XYPlot>
        </div>
    )
}

export default TimeGraph;
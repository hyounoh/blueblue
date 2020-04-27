import React, { useState, useEffect } from 'react';
import '../css/TimeGraph.css'
import '../../node_modules/react-vis/dist/style.css';
import RefreshIcon from '../icons/round_refresh_black_18dp.png';
import axios from 'axios'
import { ResponsiveBar } from '@nivo/bar'

const TimeGraph = () => {

    // Define state of wordcloud data
    const [graph, setGraph] = useState([{ "date": "0000-00-00", "count": 0 }]);

    // Set event on refresh to load wordcloud data
    const onRefresh = () => {
        axios.get('http://localhost:5001/petition-graph?recent=0')
            .then(
                response => {
                    let graph = response.data['results']['graph'];
                    setGraph(graph);
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
        console.log('TimeGraph rendered!');
        onRefresh();
    }, []);

    return (
        <div className="TimeGraph">
            <div className="Refresh" onClick={onRefresh}>
                <img src={RefreshIcon} alt="Refresh"></img>
            </div>
            <div className="PlotContainer">
                <ResponsiveBar
                    data={graph}
                    keys={['count']}
                    indexBy="date"
                    margin={{ top: 64, right: 128, bottom: 64, left: 64 }}
                    padding={0.3}
                    // colors={{ scheme: 'nivo' }}
                    colors={'#082E59'}
                    borderColor={{ from: 'color', modifiers: [['darker', -1.6]] }}
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: -45,
                        legendOffset: 32
                    }}
                    axisLeft={null}
                    labelSkipWidth={12}
                    labelSkipHeight={12}
                    labelTextColor={{ from: 'color', modifiers: [['darker', -50]] }}
                    legends={[
                        {
                            dataFrom: 'keys',
                            anchor: 'bottom-right',
                            direction: 'column',
                            justify: false,
                            translateX: 120,
                            translateY: 0,
                            itemsSpacing: 2,
                            itemWidth: 100,
                            itemHeight: 20,
                            itemDirection: 'left-to-right',
                            itemOpacity: 0.85,
                            symbolSize: 20,
                            effects: [
                                {
                                    on: 'hover',
                                    style: {
                                        itemOpacity: 1
                                    }
                                }
                            ]
                        }
                    ]}
                    animate={true}
                    motionStiffness={90}
                    motionDamping={15}
                />
            </div>
        </div>
    )
}

export default TimeGraph;
import React from 'react';
import './App.css';
import Title from './components/Title';
import Dashboard from './components/Dashboard';
import Wordcloud from './components/Wordcloud';
import PetitionList from './components/PetitionList';
import TimeGraph from './components/TimeGraph';
import Footer from './components/Footer';

function App() {

  return (
    <div className="App">
      <div className="Title">
        <Title></Title>
      </div>
      <div>
        <Dashboard></Dashboard>
      </div>
      <div className="Wordcloud">
        <Wordcloud></Wordcloud>
      </div>
      <div>
        <PetitionList></PetitionList>
      </div>
      <div>
        <TimeGraph></TimeGraph>
      </div>
      <div className="FooterArea">
        <Footer></Footer>
      </div>
    </div>
  );
}

export default App;

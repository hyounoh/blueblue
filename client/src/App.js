import React from 'react';
import './App.css';
import Title from './components/Title';
import Wordcloud from './components/Wordcloud';

function App() {

  return (
    <div className="App">
      <div className="Title">
        <Title></Title>
      </div>
      <div className="Content">
        <Wordcloud></Wordcloud>
      </div>
    </div>
  );
}

export default App;

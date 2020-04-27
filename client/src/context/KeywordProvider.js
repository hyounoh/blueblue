import React, { useState } from 'react';
import KeywordContext from './Keyword.context';

const KeywordProvider = ({ children }) => {

  const change = (currKeyword) => {
    console.log('context change is called!', currKeyword);
    setWord(currKeyword);
  };

  const initialState = {
    word: "DefaultKeyword",
    change
  };

  const [word, setWord] = useState(initialState);

  return (
    <KeywordContext.Provider value={word}>
      {children}
    </KeywordContext.Provider>
  )
}

export default KeywordProvider;
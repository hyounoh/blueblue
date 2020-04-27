import React, { useState } from 'react';
import KeywordContext from './Keyword.context';

const KeywordProvider = ({ children }) => {

  const change = (currWord) => {
    setKeyword(prevState => {
      return {
        ...prevState,
        word: currWord
      }
    });
  };

  const initialState = {
    word: "DefaultWord",
    change
  };

  const [keyword, setKeyword] = useState(initialState);

  return (
    <KeywordContext.Provider value={keyword}>
      {children}
    </KeywordContext.Provider>
  )
}

export default KeywordProvider;
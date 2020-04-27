import { createContext } from 'react';

const KeywordContext = createContext({
  word: "DefaultKeyword",
  change: () => {}
});

export default KeywordContext;
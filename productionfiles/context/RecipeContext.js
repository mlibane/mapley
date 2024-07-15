import React, { createContext, useContext, useReducer } from 'react';

const RecipeContext = createContext();

const recipeReducer = (state, action) => {
  switch (action.type) {
    case 'SET_RECIPES':
      return { ...state, recipes: action.payload };
    // Add more cases as needed
    default:
      return state;
  }
};

export const RecipeProvider = ({ children }) => {
  const [state, dispatch] = useReducer(recipeReducer, { recipes: [] });
  return (
    <RecipeContext.Provider value={{ state, dispatch }}>
      {children}
    </RecipeContext.Provider>
  );
};

export const useRecipes = () => useContext(RecipeContext);
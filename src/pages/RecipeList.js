import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RecipeCardWrapper from '../components/RecipeCardWrapper';

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await axios.get(`https://api.spoonacular.com/recipes/random?number=10&apiKey=${process.env.REACT_APP_SPOONACULAR_API_KEY}`);
        setRecipes(response.data.recipes);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to fetch recipes. Please try again later.');
        setIsLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {recipes.map(recipe => (
        <RecipeCardWrapper
          key={recipe.id}
          recipe={recipe}
          isLoading={isLoading}
          error={error}
        />
      ))}
    </div>
  );
};

export default RecipeList;
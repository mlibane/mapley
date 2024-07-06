import React, { useState, useEffect } from 'react';
import RecipeCard from '../components/RecipeCard';
import RecipeCardWrapper from '../components/RecipeCardWrapper';
import SearchBar from '../components/SearchBar';
import { fetchRecipes } from '../utils/api';

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadRecipes();
  }, []);

  const loadRecipes = async () => {
    try {
      const data = await fetchRecipes();
      setRecipes(data);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const filteredRecipes = recipes.filter(recipe =>
    recipe.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container mx-auto px-4">
      <SearchBar onSearch={setSearchTerm} />
      <RecipeCardWrapper>
        {filteredRecipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </RecipeCardWrapper>
    </div>
  );
};

export default RecipeList;
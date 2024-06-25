// src/pages/Home.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CuisineSelector from '../components/CuisineSelector';
import RecipeCard from '../components/RecipeCard';

function Home() {
  const [cuisines, setCuisines] = useState([]);
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Fetch cuisines
    setCuisines([
      { name: 'AMERICAN', image: '/static/images/image-1.png' },
      { name: 'KID FRIENDLY', image: '/static/images/image-2.png' },
      { name: 'ITALIAN', image: '/static/images/image-3.png' },
      { name: 'ASIAN', image: '/static/images/image-4.png' },
      { name: 'MEXICAN', image: '/static/images/image-5.png' },
      { name: 'SOUTHERN & SOUL FOOD', image: '/static/images/image-6.png' },
      { name: 'FRENCH', image: '/static/images/image-7.png' },
      { name: 'SOUTHWESTERN', image: '/static/images/image-8.png' },
    ]);

    // Fetch recipes from Spoonacular API
    const API_KEY = 'YOUR_SPOONACULAR_API_KEY';
    axios.get(`https://api.spoonacular.com/recipes/random?number=5&apiKey=${API_KEY}`)
      .then(response => setRecipes(response.data.recipes))
      .catch(error => console.error('Error fetching recipes:', error));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Welcome to Mapley</h1>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">What are your favorite cuisines?</h2>
      <CuisineSelector cuisines={cuisines} />
      <h2 className="text-2xl font-semibold text-gray-800 mt-12 mb-6">Just For You</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
}

export default Home;
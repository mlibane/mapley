import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Hero from '../components/Hero';
import CuisineSelector from '../components/CuisineSelector';
import RecipeCard from '../components/RecipeCard';
import SearchBar from '../components/SearchBar';

function Home() {
  const [cuisines, setCuisines] = useState([]);
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Fetch cuisines
    axios.get('/api/cuisines/')
      .then(response => setCuisines(response.data))
      .catch(error => console.error('Error fetching cuisines:', error));

    // Fetch recipes
    axios.get('/api/recipes/')
      .then(response => setRecipes(response.data))
      .catch(error => console.error('Error fetching recipes:', error));
  }, []);

  const handleSearch = (searchTerm) => {
    // Implement search functionality here
    console.log('Searching for:', searchTerm);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <Hero />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SearchBar onSearch={handleSearch} />
        <h2 className="text-2xl font-semibold text-gray-800 mt-12 mb-4">What are your favorite cuisines?</h2>
        <CuisineSelector cuisines={cuisines} />
        <div className="mt-12 bg-green-50 p-4 rounded-lg flex items-center justify-between">
          <div>
            <h3 className="font-semibold">Get our app and take us with you</h3>
            <p className="text-sm text-gray-600">Recipes, smart shopping list + more on your phone</p>
          </div>
          <button className="bg-orange-500 text-white px-4 py-2 rounded">Download For Free</button>
        </div>
        <h2 className="text-2xl font-semibold text-gray-800 mt-12 mb-6">Just For You</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {recipes.map((recipe, index) => (
            <RecipeCard key={index} recipe={recipe.recipe} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;
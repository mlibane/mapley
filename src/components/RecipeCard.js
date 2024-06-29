import React from 'react';
import { Heart } from 'lucide-react';

const RecipeCard = ({ recipe }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img src={recipe.image} alt={recipe.label} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-xl font-semibold mb-2">{recipe.label}</h3>
        <p className="text-gray-600 mb-4">Source: {recipe.source}</p>
        <div className="flex justify-between items-center">
          <a href={recipe.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
            View Recipe
          </a>
          <button className="text-gray-500 hover:text-red-500">
            <Heart className="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecipeCard;
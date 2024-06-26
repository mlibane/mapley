import React from 'react';
import { Clock, Users } from 'lucide-react';

const RecipeCard = ({ recipe }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:scale-105">
      <img 
        src={recipe.image} 
        alt={recipe.title} 
        className="w-full h-48 object-cover"
        loading="lazy"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 truncate">{recipe.title}</h3>
        <div className="flex items-center text-sm text-gray-600 mb-2">
          <Clock className="w-4 h-4 mr-1" />
          <span>{recipe.readyInMinutes} mins</span>
          <Users className="w-4 h-4 ml-4 mr-1" />
          <span>{recipe.servings} servings</span>
        </div>
        <p className="text-sm text-gray-500 mb-4 line-clamp-2">{recipe.summary}</p>
        <button className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors duration-300">
          View Recipe
        </button>
      </div>
    </div>
  );
};

export default RecipeCard;
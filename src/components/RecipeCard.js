import React from 'react';

const RecipeCard = ({ title, image, time, difficulty }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img src={image} alt={title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <div className="flex justify-between text-sm text-gray-600">
          <span>⏱️ {time} mins</span>
          <span>📊 {difficulty}</span>
        </div>
      </div>
    </div>
  );
};

export default RecipeCard;
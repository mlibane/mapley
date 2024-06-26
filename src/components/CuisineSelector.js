import React from 'react';

const cuisines = [
  { name: 'Italian', icon: '🍝' },
  { name: 'Chinese', icon: '🥡' },
  { name: 'Mexican', icon: '🌮' },
  { name: 'Japanese', icon: '🍣' },
  { name: 'Indian', icon: '🍛' },
  { name: 'American', icon: '🍔' },
  { name: 'Thai', icon: '🍜' },
  { name: 'French', icon: '🥐' },
];

const CuisineSelector = () => {
  return (
    <div className="py-12 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-8">Choose Your Cuisine</h2>
        <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-8">
          {cuisines.map((cuisine) => (
            <button
              key={cuisine.name}
              className="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300 ease-in-out"
            >
              <span className="text-4xl mb-2">{cuisine.icon}</span>
              <span className="text-sm font-medium text-gray-900">{cuisine.name}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CuisineSelector;
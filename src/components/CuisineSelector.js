import React from 'react';

const cuisines = [
  { name: 'Italian', icon: '🍝' },
  { name: 'Japanese', icon: '🍣' },
  { name: 'Mexican', icon: '🌮' },
  { name: 'Indian', icon: '🍛' },
  { name: 'Chinese', icon: '🥡' },
  { name: 'French', icon: '🥐' },
];

const CuisineSelector = () => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      {cuisines.map((cuisine) => (
        <button
          key={cuisine.name}
          className="flex flex-col items-center justify-center p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
        >
          <span className="text-4xl mb-2">{cuisine.icon}</span>
          <span className="text-sm font-medium">{cuisine.name}</span>
        </button>
      ))}
    </div>
  );
};

export default CuisineSelector;
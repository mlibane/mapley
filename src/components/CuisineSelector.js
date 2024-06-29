import React from 'react';

const CuisineSelector = ({ cuisines }) => {
  return (
    <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-8">
      {cuisines.map((cuisine) => (
        <button
          key={cuisine.name}
          className="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300 ease-in-out"
        >
          <img src={cuisine.image} alt={cuisine.name} className="w-20 h-20 rounded-full object-cover mb-2" />
          <span className="text-sm font-medium text-gray-900">{cuisine.name}</span>
        </button>
      ))}
    </div>
  );
};

export default CuisineSelector;
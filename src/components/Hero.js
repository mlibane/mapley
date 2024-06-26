import React, { useState } from 'react';
import { Search } from 'lucide-react';

const Hero = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    // Implement search functionality here
    console.log('Searching for:', searchTerm);
  };

  return (
    <div className="bg-green-50 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          <span className="block">Discover Delicious</span>
          <span className="block text-green-600">Recipes</span>
        </h1>
        <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl">
          Find and share the best recipes from around the world. Start your culinary journey today!
        </p>
        <form onSubmit={handleSearch} className="mt-8 sm:mx-auto sm:max-w-lg sm:flex">
          <div className="min-w-0 flex-1">
            <label htmlFor="search" className="sr-only">Search recipes</label>
            <input
              id="search"
              type="text"
              className="block w-full px-4 py-3 rounded-md border border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm"
              placeholder="Search recipes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="mt-3 sm:mt-0 sm:ml-3">
            <button
              type="submit"
              className="block w-full px-4 py-3 rounded-md shadow bg-green-600 text-white font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:text-sm"
            >
              <Search className="h-5 w-5 inline-block mr-2" />
              Search
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Hero;
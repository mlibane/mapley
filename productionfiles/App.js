import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Hero from './components/Hero';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';
import FeaturedRecipes from './components/FeaturedRecipes';
import RecipeList from './components/RecipeList';

const Home = () => (
  <>
    <Hero />
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-4">Featured Recipes</h2>
      <FeaturedRecipes />
      <h2 className="text-2xl font-bold mt-8 mb-4">All Recipes</h2>
      <RecipeList />
    </div>
  </>
);

const App = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex flex-grow">
          <Sidebar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/featured" element={<FeaturedRecipes />} />
              <Route path="/recipes" element={<RecipeList />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
// src/App.js
import React, { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';

const Home = lazy(() => import('./pages/Home'));
const FeaturedRecipes = lazy(() => import('./components/FeaturedRecipes'));
const RecipeList = lazy(() => import('./components/RecipeList'));

const App = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex flex-grow">
          <Sidebar />
          <ErrorBoundary>
            <main className="flex-grow">
              <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/featured" element={<FeaturedRecipes />} />
                  <Route path="/recipes" element={<RecipeList />} />
                </Routes>
              </Suspense>
            </main>
          </ErrorBoundary>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
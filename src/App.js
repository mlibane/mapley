// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Navbar />
          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
            <Switch>
              <Route exact path="/" component={Home} />
              {/* Add more routes as needed */}
            </Switch>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
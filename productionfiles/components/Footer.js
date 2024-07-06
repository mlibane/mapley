import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-mapley-dark text-white mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="hover:text-mapley-green transition-colors">Home</Link></li>
              <li><Link to="/recipes" className="hover:text-mapley-green transition-colors">Recipes</Link></li>
              <li><Link to="/about" className="hover:text-mapley-green transition-colors">About</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link to="/privacy" className="hover:text-mapley-green transition-colors">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-mapley-green transition-colors">Terms of Service</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4">
              {/* Add social media icons here */}
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-700 text-center">
          <p>&copy; 2024 Mapley. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
import React from 'react';

function Footer() {
  return (
    <footer className="bg-gray-200 p-4 mt-8">
      <div className="container mx-auto flex justify-between items-center">
        <p>&copy; 2024 Mapley. All rights reserved.</p>
        <div className="flex space-x-4">
          <a href="#" className="text-gray-600 hover:text-gray-800">Facebook</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Twitter</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Instagram</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Pinterest</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
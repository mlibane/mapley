// src/components/Sidebar.js
import React from 'react';
import { Link } from 'react-router-dom';

const sidebarItems = [
  { name: 'Meal Planning', link: '/meal-planning', icon: 'image-10.png' },
  { name: 'My Feed', link: '/my-feed', icon: 'image-11.png' },
  { name: 'Browse', link: '/browse', icon: 'image-12.png' },
  { name: 'Pro Recipes', link: '/pro-recipes', icon: 'image-13.png' },
  { name: 'Guided Recipes', link: '/guided-recipes', icon: 'image-14.png' },
  { name: 'Articles', link: '/articles', icon: 'image-15.png' },
  { name: 'Saved Recipes', link: '/saved-recipes', icon: 'image-1.png' },
  { name: 'More Tools', link: '/more-tools', icon: 'image-2.png' },
];

function Sidebar() {
  return (
    <aside className="bg-gray-50 w-64 min-h-screen shadow-md fixed left-0 top-0 z-20">
      <div className="p-4">
        <nav className="mt-5 space-y-1">
          {sidebarItems.map(item => (
            <Link
              key={item.name}
              to={item.link}
              className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-orange-50 hover:text-orange-600"
            >
              <img src={`/static/images/${item.icon}`} alt="" className="mr-3 h-6 w-6" />
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;
import React from 'react';

const recipes = [
  { id: 1, title: 'Spaghetti Carbonara', image: 'carbonara.jpg', description: 'Classic Italian pasta dish' },
  { id: 2, title: 'Chicken Tikka Masala', image: 'tikka-masala.jpg', description: 'Creamy and spicy Indian curry' },
  { id: 3, title: 'Sushi Rolls', image: 'sushi.jpg', description: 'Assorted Japanese sushi rolls' },
  { id: 4, title: 'Tacos al Pastor', image: 'tacos.jpg', description: 'Traditional Mexican street tacos' },
];

const FeaturedRecipes = () => {
  return (
    <section>
      <h2 className="text-2xl font-semibold mb-4">Featured Recipes</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {recipes.map((recipe) => (
          <div key={recipe.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <img src={recipe.image} alt={recipe.title} className="w-full h-48 object-cover" />
            <div className="p-4">
              <h3 className="text-lg font-semibold mb-2">{recipe.title}</h3>
              <p className="text-gray-600">{recipe.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default FeaturedRecipes;
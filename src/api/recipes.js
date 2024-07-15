import axios from 'axios';

const API_URL = '/api';

export const fetchRecipes = async () => {
  try {
    const response = await axios.get(`${API_URL}/recipes/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recipes:', error);
    throw error;
  }
};
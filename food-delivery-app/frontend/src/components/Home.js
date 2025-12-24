import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home = () => {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const response = await axios.get('http://localhost:5002/restaurants');
        setRestaurants(response.data);
      } catch (error) {
        console.error('Error fetching restaurants:', error);
      }
    };
    fetchRestaurants();
  }, []);

  return (
    <div className="restaurant-list">
      <h2>Available Restaurants</h2>
      {restaurants.map(restaurant => (
        <div key={restaurant.id} className="restaurant-card">
          <h3>{restaurant.name}</h3>
          <p><strong>Address:</strong> {restaurant.address}</p>
          <p><strong>Phone:</strong> {restaurant.phone}</p>
        </div>
      ))}
    </div>
  );
};

export default Home;

import React from 'react';
import { Link } from 'react-router-dom';
import main_image from '../images/main_image.jpg';

const Main = () => {
  return (
    <main className="App-main">
      <div className="landing-content">
      
        <div className="image-box">
          <img src={main_image} alt="Main image" />
        </div>
      
        <div className="text-box">
          <h2>Welcome to PawPair!</h2>
          <p>At PawPair, we believe that every pet deserves a loving home. That's why we created a matching service that connects pet lovers with shelter animals.</p>
          <p>Our service is easy to use: simply create a profile and tell us about the type of pet you're looking for. We'll then match you with shelter animals that are a good fit for your lifestyle and needs.</p>
          <p>
            <Link to="/signup" className="cta-button">
              Create a profile and get started!
            </Link>
          </p>
        </div>
      
      </div>      
    </main>
  );
};

export default Main;
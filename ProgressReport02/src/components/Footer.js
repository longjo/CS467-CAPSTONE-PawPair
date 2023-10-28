import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="App-footer">
      <nav>
        <Link to="/" className="cta-button">Home</Link> |
        <Link to="/about" className="cta-button"> About</Link> |
        <Link to="/contact" className="cta-button"> Contact Us</Link>
      </nav>
      &copy; 2023 AI Coder Team
    </footer>
  );
};

export default Footer;
import React from 'react';
import { Link } from 'react-router-dom';

import logo from '../images/logo.png';

const Header = () => {
  return (
    <header className="App-header">
        <Link to="/">
          <img src={logo} alt="PawPair Logo"/>
        </Link>  
        <nav>
          <Link to="/signup">Sign Up</Link> |
          <Link to="/login"> Log In</Link>
        </nav>
    </header>
  );
};

export default Header;
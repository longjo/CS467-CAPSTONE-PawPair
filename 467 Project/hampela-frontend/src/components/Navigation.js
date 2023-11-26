import React from 'react';
import { Link } from 'react-router-dom';


function Navigation() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="../login">Log In</Link>
      <Link to="../create-account">Create Account</Link>
      <Link to="../view-animals">Animals</Link>
      <Link to="../create-animal">Create Animal</Link>
    </nav>
  );
}

export default Navigation;

// Import dependencies
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { useState } from 'react';

// Import Components, styles, media
import Navigation from './components/Navigation';
import './App.css';

// Import Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import CreateAccountPage from './pages/CreateAccountPage';
import EditUserPage from './pages/EditUserPage';
import AnimalsPage from './pages/AnimalsPage';
import YourAccountPage from './pages/YourAccountPage';
import CreateAnimalPage from './pages/CreateAnimalPage';

// Define the function that renders the content in routes using State.
function App() {

  const [user, setUser] = useState([]);

  return (
    <>
      <Router>

        <header>
          <h1>Paw Pair</h1>
          <p>Matching Perfect Pets With Their Perfect Homes</p>
        </header>

        <Navigation></Navigation>

        <main>
          <Route path="/" exact>
            <HomePage setUser={setUser} />
          </Route>

          <Route path="/login">
            <LoginPage />
          </Route>

          <Route path="/your-account">
            <YourAccountPage />
          </Route>

          <Route path="/create-account">
            <CreateAccountPage />
          </Route>

          <Route path="/edit-user">
            <EditUserPage user={user} />
          </Route>

          <Route path="/view-animals">
            <AnimalsPage />
          </Route>

          <Route path="/create-animal">
            <CreateAnimalPage />
          </Route>

        </main>

        <footer>
          <p>2022 Adam Hampel &#169;</p>
        </footer>

      </Router>
    </>
  );
}

export default App;
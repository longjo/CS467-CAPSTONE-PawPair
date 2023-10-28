import React from 'react';
import { Link } from 'react-router-dom';
// import login_image from '../images/login_image.png';

const Main = () => {
  return (
    <main className="App-main">
      <div className="login-content">
        <div class="account-form">

          {/* <div className='image-box'>
            <img src={login_image} />
          </div> */}

          <h1>Welcome back!</h1>
        
          <form action="/create_account" method="post">          
        
            <input type="email" name="email" placeholder="Email" required/>
            <br/>
        
            <input type="password" name="password" placeholder="Password" required/>
            <br/>
        
            <input type="submit" class="cta-button" value="Log In"/>
          </form>
          <p>
            Don't have an account?
            <Link to="/signup"> Sign Up</Link>
          </p>

        </div>
      </div>     
    </main>
  );
};

export default Main;
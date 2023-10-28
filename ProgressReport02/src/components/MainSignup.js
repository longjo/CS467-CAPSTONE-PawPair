import React from 'react';
import { Link } from 'react-router-dom';
// import login_image from '../images/login_image.png';

const Main = () => {
  return (
    <main className="App-main">
      <div className="signup-content">
        <div class="account-form">

          {/* <div className='image-box'>
            <img src={login_image} />
          </div> */}

            <h1>Create a PawPair Profile</h1>
          
            <form action="/create_account" method="post">



              <div class="name-form">
                <input type="text" name="first_name" placeholder="First name" required />
                <input type="text" name="last_name" placeholder="Last name" required />
              </div>
              
          
              <input type="email" name="email" placeholder="Email" required />
          
              <br/>
          
              <input type="password" name="password" placeholder="Password" required />
          
              <br/>
          
              <input type="submit" class="cta-button" value="Create Profile" />
            </form>
            <p>
              Already have an account?
              <Link to="/login"> Log In</Link>
            </p>
          </div>
      </div>     
    </main>
  );
};

export default Main;
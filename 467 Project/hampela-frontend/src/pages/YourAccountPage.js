import React from 'react';
import { useLocation } from 'react-router-dom';

function YourAccountPage() {
    const location = useLocation();
    const user = location.state.user;

    return (
        <div>
            <h1>Your Account Information</h1>
            <p>Name: {user.name}</p>
            <p>Age: {user.age}</p>
            <p>Email: {user.email}</p>
            <p>Password: {user.password}</p>
        </div>
    );
}

export default YourAccountPage;
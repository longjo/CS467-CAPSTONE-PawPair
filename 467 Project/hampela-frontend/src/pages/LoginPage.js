import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const LoginPage = () => {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const history = useHistory();

    const loginUser = async () => {
        const user = { email, password };
        const response = await fetch('/login', {
            method: 'post',
            body: JSON.stringify(user),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 200) {
            const userData = await response.json();
            alert("Successfully logged in!");
            history.push("/your-account", { user: userData });
        } else {
            alert(`Account not found, check your email or password.`);
        }
    };


    return (
        <>
            <article>
                <h2>Log In to Your Account</h2>
                <p>Please enter your email and password below</p>
                <form onSubmit={(e) => { e.preventDefault(); }}>
                    <fieldset>
                        <legend>Account Info</legend>
                        <label for="email"> Email</label>
                        <input
                            type="text"
                            placeholder="Email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            id="email" />

                        <label for="password"> Password</label>
                        <input
                            type="text"
                            placeholder="Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            id="password" />

                        <label for="submit">
                            <button
                                type="submit"
                                onClick={loginUser}
                                id="submit"
                            >Log In</button></label>
                    </fieldset>
                </form>
            </article>
        </>
    );
}

export default LoginPage;
import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const CreateAccountPage = () => {

    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const history = useHistory();

    const addUser = async () => {
        const newUser = { name, age, email, password };
        const response = await fetch('/users', {
            method: 'post',
            body: JSON.stringify(newUser),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 201) {
            alert("Successfully added the user!");
        } else {
            alert(`Failed to add user, status code = ${response.status}`);
        }
        history.push("/");
    };


    return (
        <>
            <article>
                <h2>Create an Account</h2>
                <p>Create an account with your name, age, email and password</p>
                <form onSubmit={(e) => { e.preventDefault(); }}>
                    <fieldset>
                        <legend>Account Info</legend>
                        <label for="name">Name</label>
                        <input
                            type="text"
                            placeholder="Full Name"
                            value={name}
                            onChange={e => setName(e.target.value)}
                            id="name" />

                        <label for="age"> Age</label>
                        <input
                            type="number"
                            value={age}
                            placeholder="Age"
                            onChange={e => setAge(e.target.value)}
                            id="age" />

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
                                onClick={addUser}
                                id="submit"
                            >Add</button></label>
                    </fieldset>
                </form>
            </article>
        </>
    );
}

export default CreateAccountPage;
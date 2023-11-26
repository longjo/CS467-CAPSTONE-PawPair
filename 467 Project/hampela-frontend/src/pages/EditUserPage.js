import React from 'react';
import { useHistory } from "react-router-dom";
import { useState } from 'react';

export const EditUserPage = ({ user }) => {

    const [name, setName] = useState(user.name);
    const [age, setAge] = useState(user.age);
    const [email, setEmail] = useState(user.email);
    const [password, setPassword] = useState(user.password);

    const history = useHistory();

    const editUser = async () => {
        const response = await fetch(`/users/${user._id}`, {
            method: 'PUT',
            body: JSON.stringify({
                name: name,
                age: age,
                email: email,
                password: password
            }),
            headers: { 'Content-Type': 'application/json', },
        });

        if (response.status === 200) {
            alert("Successfully edited document!");
        } else {
            const errMessage = await response.json();
            alert(`Failed to update document. Status ${response.status}. ${errMessage.Error}`);
        }
        history.push("/");
    }

    return (
        <>
            <article>
                <h2>Edit a User</h2>
                <p>Tweak any attribute of your listed users</p>
                <form onSubmit={(e) => { e.preventDefault(); }}>
                    <fieldset>
                        <legend>Which user are you adding?</legend>
                        <label for="name">User Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={e => setName(e.target.value)}
                            id="name" />

                        <label for="age">Age</label>
                        <input
                            type="number"
                            value={age}
                            onChange={e => setAge(e.target.value)}
                            id="age" />

                        <label for="email">Email of user</label>
                        <input
                            type="number"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            id="email" />

                        <label for="password">Password of user</label>
                        <input
                            type="text"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            id="password" />

                        <label for="submit">
                            <button
                                onClick={editUser}
                                id="submit"
                            >Save</button> updates to the collection</label>
                    </fieldset>
                </form>
            </article>
        </>
    );
}
export default EditUserPage;
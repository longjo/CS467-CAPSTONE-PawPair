import React from 'react';
import Table from '../components/userTable';
import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function HomePage({ setUser }) {
    // Use the history for updating
    const history = useHistory();

    // Use state to bring in the data
    const [users, setUsers] = useState([]);

    // RETRIEVE the list of users
    const loadUsers = async () => {
        const response = await fetch('/users');
        const users = await response.json();
        setUsers(users);
    }


    // UPDATE a user
    const onEditUser = async user => {
        setUser(user);
        history.push("/edit-user");
    }


    // DELETE a user  
    const onDeleteUser = async _id => {
        const response = await fetch(`/users/${_id}`, { method: 'DELETE' });
        if (response.status === 204) {
            const getResponse = await fetch('/users');
            const users = await getResponse.json();
            setUsers(users);
        } else {
            console.error(`Failed to delete user with _id = ${_id}, status code = ${response.status}`)
        }
    }

    // LOAD the users
    useEffect(() => {
        loadUsers();
    }, []);

    // DISPLAY the users
    return (
        <>
            <article>
                <h2>List of Accounts</h2>
                <p>A list of your users & their details</p>
                <Table
                    users={users}
                    onEdit={onEditUser}
                    onDelete={onDeleteUser}
                />
            </article>
        </>
    );
}

export default HomePage;
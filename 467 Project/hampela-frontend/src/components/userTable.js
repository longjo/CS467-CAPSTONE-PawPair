import React from 'react';
import Row from './userRow';

function Table({ users, onDelete, onEdit }) {
    return (
        <table id="users">
            <caption>Create and Edit Accounts</caption>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Email</th>
                    <th>Password</th>
                    <th>Delete</th>
                    <th>Edit</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user, i) =>
                    <Row
                        user={user}
                        key={i}
                        onDelete={onDelete}
                        onEdit={onEdit}
                    />)}
            </tbody>
        </table>
    );
}

export default Table;
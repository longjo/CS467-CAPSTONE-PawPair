import React from 'react';
import { MdDeleteForever, MdEdit } from 'react-icons/md';

function Row({ user, onEdit, onDelete }) {
    return (
        <tr>
            <td>{user.name}</td>
            <td>{user.age}</td>
            <td>{user.email}</td>
            <td>{user.password}</td>
            <td><MdDeleteForever onClick={() => onDelete(user._id)} /></td>
            <td><MdEdit onClick={() => onEdit(user)} /></td>
        </tr>
    );
}

export default Row;
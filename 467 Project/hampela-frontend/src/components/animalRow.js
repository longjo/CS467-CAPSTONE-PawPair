import React from 'react';

function Row({ pet, onDelete, onEdit }) {
    return (
        <tr>
            <td>{pet.name}</td>
            <td>{pet.type}</td>
            <td>{pet.age}</td>
            <td><img src={pet.photo} alt={pet.name} style={{ width: "100px" }} /></td> {/* New cell for the photo */}
            <td><button onClick={() => onDelete(pet._id)}>Delete</button></td>
            <td><button onClick={() => onEdit(pet)}>Edit</button></td>
        </tr>
    );
}

export default Row;
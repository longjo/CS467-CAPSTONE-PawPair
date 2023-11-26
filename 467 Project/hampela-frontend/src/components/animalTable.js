import React from 'react';
import Row from './animalRow';

function Table({ pets, onDelete, onEdit }) {
    return (
        <table id="pets">
            <caption>Create and Edit Animals</caption>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Age</th>
                    <th>Photo</th> {/* New table header for Photo */}
                    <th>Delete</th>
                    <th>Edit</th>
                </tr>
            </thead>
            <tbody>
                {pets.map((pet, i) =>
                    <Row
                        pet={pet}
                        key={i}
                        onDelete={onDelete}
                        onEdit={onEdit}
                    />)}
            </tbody>
        </table>
    );
}

export default Table;
import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const CreateAnimalPage = () => {

    const [name, setName] = useState('');
    const [type, setType] = useState('');
    const [age, setAge] = useState('');
    const [photo, setPhoto] = useState(''); // New state variable for the photo URL

    const history = useHistory();

    const addAnimal = async () => {
        const newAnimal = { name, type, age, photo }; // Include the photo URL in the new animal object
        const response = await fetch('/pets', {
            method: 'post',
            body: JSON.stringify(newAnimal),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 201) {
            alert("Successfully added the pet!");
        } else {
            alert(`Failed to add pet, status code = ${response.status}`);
        }
        history.push("/");
    };


    return (
        <>
            <article>
                <h2>Add a Pet</h2>
                <p>Add a Pet With its Name, Species, Age, and Photo.</p>
                <form onSubmit={(e) => { e.preventDefault(); }}>
                    <fieldset>
                        <legend>Pet Info</legend>
                        <label for="name">Name</label>
                        <input
                            type="text"
                            placeholder="Pet Name"
                            value={name}
                            onChange={e => setName(e.target.value)}
                            id="name" />

                        <label for="type"> Type</label>
                        <input
                            type="text"
                            value={type}
                            placeholder="Type"
                            onChange={e => setType(e.target.value)}
                            id="type" />

                        <label for="age"> Age</label>
                        <input
                            type="number"
                            placeholder="Age"
                            value={age}
                            onChange={e => setAge(e.target.value)}
                            id="age" />

                        <label for="photo"> Photo</label> {/* New label for the photo URL */}
                        <input
                            type="text"
                            placeholder="Photo URL"
                            value={photo}
                            onChange={e => setPhoto(e.target.value)}
                            id="photo" /> {/* New input field for the photo URL */}

                        <label for="submit">
                            <button
                                type="submit"
                                onClick={addAnimal}
                                id="submit"
                            >Add</button></label>
                    </fieldset>
                </form>
            </article>
        </>
    );
}

export default CreateAnimalPage;
import React from 'react';
import Table from '../components/animalTable';
import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function AnimalsPage({ setPet }) {
    // Use the history for updating
    const history = useHistory();

    // Use state to bring in the data
    const [pets, setPets] = useState([]);

    // RETRIEVE the list of pets
    const loadPets = async () => {
        const response = await fetch('/pets');
        const pets = await response.json();
        setPets(pets);
    }


    // UPDATE a pet
    const onEditPet = async pet => {
        setPet(pets);
        history.push("/edit-pet");
    }


    // DELETE a pet  
    const onDeletePet = async _id => {
        const response = await fetch(`/pets/${_id}`, { method: 'DELETE' });
        if (response.status === 204) {
            const getResponse = await fetch('/pets');
            const pets = await getResponse.json();
            setPets(pets);
        } else {
            console.error(`Failed to delete pet with _id = ${_id}, status code = ${response.status}`)
        }
    }

    // LOAD the pets
    useEffect(() => {
        loadPets();
    }, []);

    // DISPLAY the pets
    return (
        <>
            <article>
                <h2>List of Pets</h2>
                <p>A list of pets & their details</p>
                <Table
                    pets={pets}
                    onEdit={onEditPet}
                    onDelete={onDeletePet}
                />
            </article>
        </>
    );
}

export default AnimalsPage;
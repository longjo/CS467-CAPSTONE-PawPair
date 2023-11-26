import { createPet } from './pets-model.mjs';

const populatePets = async () => {
    const petsData = [
        { name: 'Fluffy', type: 'Cat', age: 2, photo: 'https://live.staticflickr.com/8482/8243537591_4d4aa16a4e_b.jpg' },
        { name: 'Rover', type: 'Dog', age: 3, photo: 'https://live.staticflickr.com/8594/28298815283_6c9262fb2b_b.jpg' }
        // Add more pets here
    ];

    for (const petData of petsData) {
        await createPet(petData.name, petData.type, petData.age, petData.photo); // Pass the photo URL to createPet
    }

    console.log('Pets populated successfully.');
};

populatePets().catch(err => console.error('Error populating pets:', err));
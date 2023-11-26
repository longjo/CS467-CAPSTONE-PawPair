import mongoose from 'mongoose';
import 'dotenv/config';

const {createConnection} = mongoose;
//mongodb://localhost:3000/pets
// Connect based on the .env file parameters.
const petConnection = mongoose.createConnection(
    process.env.MONGODB_CONNECT_STRING_PETS,
    { useNewUrlParser: true, useUnifiedTopology: true }
);
//const db = mongoose.connection;

// Confirm that the database has connected and print a message in the console.
petConnection.once("open", (err) => {
    if (err) {
        res.status(500).json({ error: '500:Connection to the server failed.' });
    } else {
        console.log('Successfully connected to MongoDB Pets collection using Mongoose.');
    }
});

// Define the collection's schema
const petSchema = mongoose.Schema({
    name: { type: String, required: true },
    type: { type: String, required: true }, // e.g., 'cat', 'dog'
    age: { type: Number, required: true },
    photo: { type: String, required: false } // New field for the photo URL
    // Add more fields as needed
});

// Compile the model from the schema
const Pet = petConnection.model('Pet', petSchema);

// CREATE model
const createPet = async (name, type, age, photo) => {
    console.log('Creating pet:', name, type, age, photo);
    const pet = new Pet({
        name: name,
        type: type,
        age: age,
        photo: photo
    });
    return pet.save().catch(err => console.error('Error saving pet:', err));
}

// RETRIEVE models
// Retrieve based on a filter and return a promise
const findPets = async (filter) => {
    const query = Pet.find(filter);
    return query.exec();
}

// Retrieve based on the ID and return a promise
const findPetById = async (_id) => {
    const query = Pet.findById(_id);
    return query.exec();
}

// DELETE model based on ID
const deleteById = async (_id) => {
    const result = await Pet.deleteOne({ _id: _id });
    return result.deletedCount;
};

// REPLACE model
const replacePet = async (_id, name, type, age, photo) => {
    const result = await Pet.replaceOne({ _id: _id }, {
        name: name,
        type: type,
        age: age,
        photo: photo
    });
    return result.modifiedCount;
}

// Export our variables for use in the controller file
export { Pet, createPet, findPets, findPetById, deleteById, replacePet }
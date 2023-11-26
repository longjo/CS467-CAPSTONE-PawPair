// Import dependencies.
import mongoose from 'mongoose';
import 'dotenv/config';

const {createConnection} = mongoose;
//mongodb://localhost:3000/users
// Connect based on the .env file parameters.
const userConnection = mongoose.createConnection(
    process.env.MONGODB_CONNECT_STRING_USERS,
    { useNewUrlParser: true, useUnifiedTopology: true }
);
//const db = mongoose.connection;

// Confirm that the database has connected and print a message in the console.
userConnection.once("open", (err) => {
    if (err) {
        res.status(500).json({ error: '500:Connection to the server failed.' });
    } else {
        console.log('Successfully connected to MongoDB Users collection using Mongoose.');
    }
});

/*Define the collection's schema.
Setting "required" to be true, means that if you want to create a new
document into this collection, it must have a name, reps, weight, etc..*/
const userSchema = mongoose.Schema({
    name: { type: String, required: true },
    age: { type: Number, required: true },
    email: { type: String, required: true },
    password: { type: String, required: false }
});

// Compile the model from the schema.
const User = userConnection.model('User', userSchema);


// CREATE model *****************************************
const createUser = async (name, age, email, password) => {
    const user = new User({
        name: name,
        age: age,
        email: email,
        password: password
    });
    return user.save();
}


// RETRIEVE models *****************************************
// Retrieve based on a filter and return a promise.
const findUsers = async (filter) => {
    const query = User.find(filter);
    return query.exec();
}

// Retrieve based on the ID and return a promise.
const findUserById = async (_id) => {
    const query = User.findById(_id);
    return query.exec();
}


// DELETE model based on ID  *****************************************
const deleteById = async (_id) => {
    const result = await User.deleteOne({ _id: _id });
    return result.deletedCount;
};


// REPLACE model *****************************************************
const replaceUser = async (_id, name, age, email, password) => {
    const result = await User.replaceOne({ _id: _id }, {
        name: name,
        age: age,
        email: email,
        password: password,
    });
    return result.modifiedCount;
}


// Export our variables for use in the controller file.
export { User, createUser, findUsers, findUserById, replaceUser, deleteById }
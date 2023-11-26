import 'dotenv/config';
import express from 'express';
//import multer from 'multer';
import * as users from './users-model.mjs';
import authRoutes from './auth-routes.mjs'; // Import your auth routes
import * as pets from './pets-model.mjs';

const PORT = process.env.PORT;
const app = express();
app.use(express.json());
app.use('/', authRoutes);


const validator = (name, age, email, password) => {
    if (name === undefined || name === null || name.length <= 0)
        return false;

    if (age === undefined || age <= 0 || typeof age !== Number)
        return false;

    if (email === undefined || email.length <= 0)
        return false;

    if ((password === undefined) || password === null || password.length <= 0)
        return false;

    else
        return true;
}



// CREATE controller ******************************************
app.post('/users', (req, res) => {
    if (req.body.name.length <= 0 || req.body.age <= 0 || req.body.email.length <= 0 || req.body.password.length <= 0)
        res.status(400).json({ Error: "Invalid Request" });

    else {
        users.createUser(
            req.body.name,
            req.body.age,
            req.body.email,
            req.body.password
        )
            .then(user => {
                if (req.body.name.length > 0 || req.body.age > 0
                    || req.body.email.length > 0) {
                    res.status(201).json(user);
                } else {
                    res.status(400).json({ Error: "Invalid Request" });
                }
            })
            .catch(error => {
                console.log(error);
                res.status(400).json({ error: 'Creation of a document failed due to invalid syntax.' });
            });
    }
});


// RETRIEVE controller ****************************************************
// GET users by ID
app.get('/users/:_id', (req, res) => {
    const userId = req.params._id;
    users.findUserById(userId)
        //If promise is resolved, it is set to the value of user
        .then(user => {
            if (user !== null) {
                res.json(user);
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            res.status(400).json({ Error: 'Request to retrieve document failed' });
        });

});


// GET users filtered by name, age, email, password
app.get('/users', (req, res) => {
    let filter = {};
    // filter by name
    if (req.query.name !== undefined) {
        filter = { name: req.query.name };
    }
    // filter by age
    if (req.query.age !== undefined) {
        filter = { age: req.query.age };
    }
    // filter by email
    if (req.query.email !== undefined) {
        filter = { email: req.query.email };
    }
    // filter by password
    if (req.query.password !== undefined) {
        filter = { password: req.query.password };
    }
    users.findUsers(filter, '', 0)
        .then(users => {
            res.send(users);
        })
        .catch(error => {
            console.error(error);
            res.send({ Error: 'Request to retrieve documents failed' });
        });
});

// DELETE Controller ******************************
app.delete('/users/:_id', (req, res) => {
    users.deleteById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request to delete a document failed' });
        });
});

// UPDATE controller ************************************
app.put('/users/:_id', (req, res) => {
    users.replaceUser(
        req.params._id,
        req.body.name,
        req.body.age,
        req.body.email,
        req.body.password
    )
        .then(numUpdated => {
            if (numUpdated === 1) {
                res.status(200).json({
                    _id: req.params._id,
                    name: req.body.name,
                    age: req.body.age,
                    email: req.body.email,
                    password: req.body.password
                })
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Request to update a document failed' });
        });
}
);


// CREATE controller for pets
app.post('/pets', (req, res) => {
    console.log('Post request received');
    if (req.body.name.length <= 0 || req.body.type.length <= 0 || req.body.age.length <= 0)
        res.status(400).json({ Error: "Invalid Request" })
    else {
        pets.createPet(
            req.body.name,
            req.body.type,
            req.body.age,
            req.body.photo
        )
            .then(pet => {
                console.log('Created pet:', pet);
                if (req.body.name.length > 0 || req.body.type > 0
                    || req.body.age.length > 0) {
                    res.status(201).json(pet);
                } else {
                    res.status(400).json({ Error: "Invalid Request" });
                }
            })
            .catch(error => {
                console.log(error);
                res.status(400).json({ error: 'Creation of a document failed due to invalid syntax.' });
            });
    }
});

// RETRIEVE controller ****************************************************
// GET pets by ID
app.get('/pets/:_id', (req, res) => {
    const petId = req.params._id;
    pets.findPetById(petId)
        //If promise is resolved, it is set to the value of pet
        .then(pet => {
            if (pet !== null) {
                res.json(pet);
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            res.status(400).json({ Error: 'Request to retrieve document failed' });
        });

});

// GET pets filtered by name, type, age
app.get('/pets', (req, res) => {
    let filter = {};
    // filter by name
    if (req.query.name !== undefined) {
        filter = { name: req.query.name };
    }
    // filter by type
    if (req.query.type !== undefined) {
        filter = { type: req.query.type };
    }
    // filter by age
    if (req.query.age !== undefined) {
        filter = { age: req.query.age };
    }
    // filter by photo
    if (req.query.photo !== undefined) {
        filter = { photo: req.query.photo };
    }
    pets.findPets(filter, '', 0)
        .then(pets => {
            res.send(pets);
        })
        .catch(error => {
            console.error(error);
            res.send({ Error: 'Request to retrieve documents failed' });
        });
});

// DELETE Controller ******************************
app.delete('/pets/:_id', (req, res) => {
    pets.deleteById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request to delete a document failed' });
        });
});

// UPDATE controller ************************************
app.put('/pets/:_id', (req, res) => {
    pets.replacePet(
        req.params._id,
        req.body.name,
        req.body.type,
        req.body.age,
        req.body.photo
    )
        .then(numUpdated => {
            if (numUpdated === 1) {
                res.status(200).json({
                    _id: req.params._id,
                    name: req.body.name,
                    type: req.body.type,
                    age: req.body.age,
                    photo: req.body.photo
                })
            } else {
                res.status(404).json({ Error: 'Document not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Request to update a document failed' });
        });
}
);


app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});
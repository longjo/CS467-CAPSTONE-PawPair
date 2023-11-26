import express from 'express';
import * as users from './users-model.mjs'; // Import all named exports from users-model.mjs
import { User } from './users-model.mjs';

const router = express.Router();

router.post('/login', async (req, res) => {
    console.log('Login request data:', req.body); // Log the request data

    try {
        const user = await User.findOne({ email: req.body.email });
        console.log('Found user:', user); // Log the found user
        if (!user) {
            return res.status(401).send({ error: 'Login failed! Check authentication credentials' });
        }
        if (req.body.password !== user.password) { // Replace with your password checking logic
            return res.status(401).send({ error: 'Login failed! Check authentication credentials' });
        }
        //res.send(user);
        res.status(200).json(user);
    } catch (error) {
        console.log('Error during login:', error); // Log any errors
        res.status(400).send(error);
    }
});


export default router;
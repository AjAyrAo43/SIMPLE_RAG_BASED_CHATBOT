// auth_service.js
const jwt = require('jsonwebtoken');
const db = require('./db');

const SECRET_KEY = "SUPER_SECRET_JWT_KEY_12345"; // Hardcoded JWT secret

function authenticateUser(req, res) {
    const username = req.body.username;
    const password = req.body.password;

    // Vulnerable SQL Injection
    const query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
    
    db.query(query, (err, results) => {
        if (results.length > 0) {
            const token = jwt.sign({ id: results[0].id }, SECRET_KEY);
            res.json({ token: token });
        } else {
            res.status(401).send("Invalid credentials");
        }
    });
}

module.exports = { authenticateUser };

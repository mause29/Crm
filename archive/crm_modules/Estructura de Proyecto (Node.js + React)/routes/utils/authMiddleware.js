const jwt = require('jsonwebtoken');

function verifyToken(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) return res.status(401).json({ message: "No token provided" });

    jwt.verify(token, 'SECRET_KEY', (err, decoded) => {
        if (err) return res.status(403).json({ message: "Failed to authenticate token" });
        req.user = decoded;
        next();
    });
}

function checkRole(roles) {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({ message: "Access denied" });
        }
        next();
    }
}

module.exports = { verifyToken, checkRole };

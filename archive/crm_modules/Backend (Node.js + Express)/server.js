const express = require('express');
const cors = require('cors');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http, { cors: { origin: "*" } });
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');

app.use(cors());
app.use(bodyParser.json());

const SECRET = 'mi_clave_secreta';

// Simulación base de datos
let users = [
    { id: 1, name: 'Admin', role: 'admin', email: 'admin@crm.com', password: '1234' },
    { id: 2, name: 'User', role: 'user', email: 'user@crm.com', password: '1234' }
];

// Middleware de autenticación
function auth(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) return res.status(401).json({ message: 'No token provided' });
    jwt.verify(token, SECRET, (err, decoded) => {
        if (err) return res.status(401).json({ message: 'Invalid token' });
        req.user = decoded;
        next();
    });
}

// Login
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const user = users.find(u => u.email === email && u.password === password);
    if (!user) return res.status(401).json({ message: 'Usuario o contraseña incorrecta' });
    const token = jwt.sign({ id: user.id, role: user.role, name: user.name }, SECRET, { expiresIn: '8h' });
    res.json({ token, role: user.role, name: user.name });
});

// Roles y permisos
app.get('/dashboard', auth, (req, res) => {
    if(req.user.role !== 'admin') return res.status(403).json({ message: 'Acceso denegado' });
    res.json({ message: 'Datos de dashboard solo para administradores' });
});

// Notificaciones push con Socket.io
io.on('connection', (socket) => {
    console.log('Usuario conectado');
    socket.on('notify', (msg) => {
        io.emit('receive_notification', msg);
    });
});

http.listen(5000, () => console.log('Servidor backend corriendo en puerto 5000'));

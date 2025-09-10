const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const socketIo = require('socket.io');
const bodyParser = require('body-parser');

const userRoutes = require('./routes/metrics');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: "*" } });

app.use(bodyParser.json());
app.use('/api', userRoutes);
app.set('io', io); // permitir usar io en rutas

mongoose.connect('mongodb://localhost:27017/gamification', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('DB Conectada')).catch(console.error);

server.listen(3000, () => console.log('Server corriendo en http://localhost:3000'));

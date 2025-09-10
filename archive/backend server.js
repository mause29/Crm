// backend/server.js
const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const app = express();
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server, { cors: { origin: '*' } });

const gamificationRouter = require('./routes/gamification');
app.use(express.json());
app.use('/gamification', gamificationRouter);

// Conexión a MongoDB
mongoose.connect('mongodb://localhost:27017/gamification', { useNewUrlParser: true, useUnifiedTopology: true });

// Socket.IO: Notificaciones en tiempo real
io.on('connection', (socket) => {
    console.log('Usuario conectado: ' + socket.id);
    socket.on('disconnect', () => console.log('Usuario desconectado: ' + socket.id));
});

// Exportamos io para usar en rutas
module.exports.io = io;

server.listen(3000, () => console.log('Servidor corriendo en puerto 3000'));

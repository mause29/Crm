// backend/src/index.js (Socket.IO Setup)
import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
app.use(cors());
const server = http.createServer(app);
export const io = new Server(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
  console.log('Usuario conectado:', socket.id);
  socket.on('join', (userId) => socket.join(`user_${userId}`));
});

server.listen(3000, () => console.log('Servidor corriendo en 3000'));

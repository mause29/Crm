// backend/src/services/notifications.js
import { Server } from 'socket.io';

export default function notificationService(app) {
  const io = new Server(app.listen(), { cors: { origin: '*' } });

  io.on('connection', (socket) => {
    console.log('Usuario conectado a notificaciones');
    socket.on('disconnect', () => console.log('Usuario desconectado'));
  });

  return io;
}

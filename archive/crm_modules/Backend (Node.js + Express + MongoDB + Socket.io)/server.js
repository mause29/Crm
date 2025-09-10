// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

app.use(express.json());
app.use(cors());

// Conectar MongoDB
mongoose.connect('mongodb://localhost:27017/gamificacion', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Schema Usuarios
const userSchema = new mongoose.Schema({
  name: String,
  points: { type: Number, default: 0 },
  badges: [String],
  weeklyChallenges: [{ challenge: String, completed: Boolean }],
});

const User = mongoose.model('User', userSchema);

// Crear usuario
app.post('/user', async (req, res) => {
  const user = new User(req.body);
  await user.save();
  io.emit('updateRanking'); // notificación a todos
  res.send(user);
});

// Obtener ranking
app.get('/users', async (req, res) => {
  const users = await User.find().sort({ points: -1 });
  res.send(users);
});

// Completar challenge
app.post('/user/:id/complete-challenge', async (req, res) => {
  const { challenge, points, badge } = req.body;
  const user = await User.findById(req.params.id);

  const ch = user.weeklyChallenges.find(c => c.challenge === challenge);
  if (ch) ch.completed = true;

  user.points += points || 0;
  if (badge && !user.badges.includes(badge)) user.badges.push(badge);

  await user.save();
  io.emit('updateRanking'); // notificación de cambio
  res.send(user);
});

// Retos semanales automáticos (ejemplo simple)
const weeklyChallenges = [
  { challenge: "Cerrar 5 ventas", points: 50, badge: "Vendedor Pro" },
  { challenge: "Atender 10 tickets", points: 30, badge: "Soporte Estrella" },
];

setInterval(async () => {
  const users = await User.find();
  for (const user of users) {
    user.weeklyChallenges = weeklyChallenges.map(ch => ({ ...ch, completed: false }));
    await user.save();
  }
  io.emit('newChallenges');
}, 7 * 24 * 60 * 60 * 1000); // cada semana

// Socket.io conexión
io.on('connection', socket => {
  console.log('Cliente conectado:', socket.id);
});

server.listen(5000, () => console.log('Servidor corriendo en puerto 5000'));

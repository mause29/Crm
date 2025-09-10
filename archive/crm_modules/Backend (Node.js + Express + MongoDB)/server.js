// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Conectar a MongoDB
mongoose.connect('mongodb://localhost:27017/gamificacion', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Schemas
const userSchema = new mongoose.Schema({
  name: String,
  points: { type: Number, default: 0 },
  badges: [String],
  weeklyChallenges: [{ challenge: String, completed: Boolean }],
});

const User = mongoose.model('User', userSchema);

// Rutas API
app.post('/user', async (req, res) => {
  const user = new User(req.body);
  await user.save();
  res.send(user);
});

app.get('/users', async (req, res) => {
  const users = await User.find().sort({ points: -1 }); // ranking
  res.send(users);
});

app.post('/user/:id/complete-challenge', async (req, res) => {
  const { challenge, points, badge } = req.body;
  const user = await User.findById(req.params.id);

  // Marcar challenge como completado
  const ch = user.weeklyChallenges.find(c => c.challenge === challenge);
  if (ch) ch.completed = true;

  // Añadir puntos y badge
  user.points += points || 0;
  if (badge && !user.badges.includes(badge)) user.badges.push(badge);

  await user.save();
  res.send(user);
});

// Servidor
app.listen(5000, () => console.log('Servidor corriendo en puerto 5000'));

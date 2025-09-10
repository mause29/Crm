// server.js
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(cors());
app.use(express.json());

// Roles y permisos simulados
const users = [
  { id: 1, name: "Admin", role: "admin" },
  { id: 2, name: "Usuario", role: "user" }
];

// Endpoint para obtener datos de usuario
app.get("/users", (req, res) => {
  res.json(users);
});

// Notificaciones en tiempo real
io.on("connection", (socket) => {
  console.log("Usuario conectado:", socket.id);
  socket.on("sendNotification", (data) => {
    io.emit("receiveNotification", data);
  });
});

server.listen(4000, () => console.log("Servidor corriendo en puerto 4000"));

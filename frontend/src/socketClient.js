import { io } from "socket.io-client";

const SOCKET_SERVER_URL = "/socket.io";

const socket = io(SOCKET_SERVER_URL, {
  transports: ["websocket", "polling"],
});

socket.on("connect", () => {
  console.log("Connected to Socket.IO server with id:", socket.id);
});

socket.on("disconnect", () => {
  console.log("Disconnected from Socket.IO server");
});

export default socket;

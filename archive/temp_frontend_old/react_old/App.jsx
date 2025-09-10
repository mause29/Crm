// App.jsx
import React, { useState, useEffect } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { HotKeys } from "react-hotkeys";
import io from "socket.io-client";
import "./index.css";

const socket = io("http://localhost:4000");

const roles = {
  admin: ["edit", "view"],
  user: ["view"]
};

// Widget draggable
const Widget = ({ id, name, moveWidget }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "WIDGET",
    item: { id },
    collect: (monitor) => ({ isDragging: !!monitor.isDragging() })
  }));
  return (
    <div
      ref={drag}
      className={`bg-blue-400 p-4 rounded m-2 shadow-md cursor-move ${
        isDragging ? "opacity-50" : "opacity-100"
      }`}
    >
      {name}
    </div>
  );
};

const Dashboard = ({ user }) => {
  const [widgets, setWidgets] = useState([
    { id: 1, name: "Ventas" },
    { id: 2, name: "Leads" },
    { id: 3, name: "Tickets" }
  ]);
  const [, drop] = useDrop(() => ({
    accept: "WIDGET",
    drop: (item) => moveWidget(item.id),
  }));

  const moveWidget = (id) => {
    // Ejemplo simple de reorder
    setWidgets((prev) => [...prev.sort(() => Math.random() - 0.5)]);
  };

  return (
    <div ref={drop} className="p-4 grid grid-cols-3 gap-4 min-h-screen">
      {widgets.map((w) => (
        <Widget key={w.id} {...w} moveWidget={moveWidget} />
      ))}
    </div>
  );
};

function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState("light");
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    fetch("http://localhost:4000/users")
      .then((res) => res.json())
      .then((data) => setUser(data[0]));

    socket.on("receiveNotification", (data) => {
      setNotifications((prev) => [...prev, data]);
    });
  }, []);

  const keyMap = {
    TOGGLE_THEME: "ctrl+t",
  };

  const handlers = {
    TOGGLE_THEME: () => setTheme(theme === "light" ? "dark" : "light"),
  };

  return (
    <HotKeys keyMap={keyMap} handlers={handlers}>
      <div className={`${theme === "dark" ? "bg-gray-900 text-white" : "bg-white text-black"} min-h-screen transition-colors duration-500`}>
        <header className="p-4 flex justify-between items-center shadow-md">
          <h1>CRM Dashboard - {user?.role}</h1>
          <button
            className="bg-blue-500 px-4 py-2 rounded text-white"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          >
            Cambiar Tema
          </button>
        </header>

        <DndProvider backend={HTML5Backend}>
          <Dashboard user={user} />
        </DndProvider>

        <div className="fixed bottom-4 right-4 space-y-2">
          {notifications.map((n, i) => (
            <div key={i} className="bg-green-500 text-white p-2 rounded shadow-md">
              {n.message}
            </div>
          ))}
        </div>

        <button
          className="fixed bottom-4 left-4 bg-yellow-500 p-2 rounded"
          onClick={() => socket.emit("sendNotification", { message: "Nueva notificación" })}
        >
          Enviar Notificación
        </button>
      </div>
    </HotKeys>
  );
}

export default App;

// frontend/src/App.jsx
import React, { useEffect, useState } from 'react';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import { socketConnect } from './services/socket';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const socket = socketConnect();
    socket.on('notification', (data) => {
      console.log('Nueva notificación:', data);
    });
  }, []);

  return (
    <div className="App">
      {user ? <Dashboard user={user} /> : <Login setUser={setUser} />}
    </div>
  );
}

export default App;

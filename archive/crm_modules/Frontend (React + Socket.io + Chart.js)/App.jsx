// App.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import { Chart } from 'react-chartjs-2';

const socket = io('http://localhost:5000');

function App() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const res = await axios.get('http://localhost:5000/users');
    setUsers(res.data);
  };

  useEffect(() => {
    fetchUsers();

    socket.on('updateRanking', fetchUsers);
    socket.on('newChallenges', () => alert('¡Nuevos retos semanales disponibles!'));

    return () => {
      socket.off('updateRanking');
      socket.off('newChallenges');
    };
  }, []);

  const data = {
    labels: users.map(u => u.name),
    datasets: [
      {
        label: 'Puntos',
        data: users.map(u => u.points),
        backgroundColor: 'rgba(75,192,192,0.6)',
      },
    ],
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Ranking Gamificación</h1>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Puntos</th>
            <th>Badges</th>
            <th>Retos</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u._id}>
              <td>{u.name}</td>
              <td>{u.points}</td>
              <td>{u.badges.join(', ')}</td>
              <td>
                {u.weeklyChallenges.map(c => (
                  <div key={c.challenge}>
                    {c.challenge} - {c.completed ? '✅' : '❌'}
                  </div>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Gráfico de Puntos</h2>
      <Chart type="bar" data={data} />
    </div>
  );
}

export default App;

import React, { useEffect, useState } from 'react';
import { fetchLeaderboard } from '../services/api';

const Leaderboard = () => {
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    async function loadLeaders() {
      const data = await fetchLeaderboard();
      setLeaders(data);
    }
    loadLeaders();
  }, []);

  return (
    <div className="leaderboard">
      <h2>Ranking del Equipo</h2>
      <ul>
        {leaders.map((user, index) => (
          <li key={user.id}>{index + 1}. {user.name} - {user.points} pts</li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;

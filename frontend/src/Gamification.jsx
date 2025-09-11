import React, { useEffect, useState } from 'react';

const Gamification = () => {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch achievements data from backend API
    const token = localStorage.getItem('token');
    fetch('http://localhost:8000/gamification/achievements', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Error al cargar logros');
        }
        return response.json();
      })
      .then((data) => {
        setAchievements(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6">Cargando logros...</div>;
  }

  return (
    <div className="p-6 bg-gradient-to-r from-purple-700 via-pink-600 to-red-500 min-h-screen text-white">
      <h2 className="text-3xl font-bold mb-6">Gamificación</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {achievements.map((ach) => (
          <div key={ach.id} className="bg-white bg-opacity-20 rounded-lg p-4 shadow-lg flex flex-col items-center">
            <div className="text-5xl mb-4">{ach.badge_icon}</div>
            <h3 className="text-xl font-semibold">{ach.name}</h3>
            <p className="text-sm">{ach.description}</p>
            <p className="mt-2 text-sm font-bold">Puntos requeridos: {ach.points_required}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Gamification;

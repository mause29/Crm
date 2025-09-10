// frontend/src/components/Card.jsx
import React from 'react';

export default function Card({ title, value, icon, color }) {
  return (
    <div className={`p-4 rounded-2xl shadow-lg bg-white flex items-center gap-4 border-l-4 border-${color}-500`}>
      <div className={`text-${color}-500 text-3xl`}>{icon}</div>
      <div>
        <h2 className="text-gray-700 font-bold">{title}</h2>
        <p className="text-gray-500 text-xl">{value}</p>
      </div>
    </div>
  );
}

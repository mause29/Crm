// frontend/src/pages/BIDashboard.jsx
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { getDashboardData } from '../services/api';

export default function BIDashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const result = await getDashboardData();
      setData(result.salesByDay);
    }
    fetchData();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Ventas Semanales</h1>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="sales" fill="#4ade80" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

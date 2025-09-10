// frontend/src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import { FaUserAlt, FaDollarSign, FaChartLine } from 'react-icons/fa';
import { getDashboardData } from '../services/api';

export default function Dashboard({ user }) {
  const [stats, setStats] = useState({ users: 0, revenue: 0, sales: 0 });

  useEffect(() => {
    async function fetchData() {
      const data = await getDashboardData();
      setStats(data);
    }
    fetchData();
  }, []);

  return (
    <div className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card title="Usuarios Activos" value={stats.users} icon={<FaUserAlt />} color="blue" />
      <Card title="Ingresos" value={`$${stats.revenue}`} icon={<FaDollarSign />} color="green" />
      <Card title="Ventas Totales" value={stats.sales} icon={<FaChartLine />} color="purple" />
    </div>
  );
}

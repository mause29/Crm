import React, { useEffect, useState } from 'react';
import { fetchKPIs } from '../services/api';

const Dashboard = () => {
  const [kpis, setKpis] = useState([]);

  useEffect(() => {
    async function loadKPIs() {
      const data = await fetchKPIs();
      setKpis(data);
    }
    loadKPIs();
  }, []);

  return (
    <div className="dashboard">
      <h1>Dashboard en Tiempo Real</h1>
      <div className="kpi-cards">
        {kpis.map(kpi => (
          <div key={kpi.id} className="kpi-card">
            <h3>{kpi.title}</h3>
            <p>{kpi.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;

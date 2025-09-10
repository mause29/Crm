import React from 'react';
import { Chart } from 'react-chartjs-2';

export default function Dashboard() {
  const data = {
    labels: ['New', 'In Progress', 'Won', 'Lost'],
    datasets: [
      {
        label: 'Oportunidades',
        data: [12, 19, 7, 3],
        backgroundColor: ['#36A2EB','#FFCE56','#4BC0C0','#FF6384']
      }
    ]
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <Chart type="bar" data={data} />
    </div>
  );
}

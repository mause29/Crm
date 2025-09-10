import React, { useState, useEffect } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const SalesReports = () => {
  const [salesData, setSalesData] = useState([]);

  useEffect(() => {
    const fetchSalesData = async () => {
      try {
        const response = await fetch('http://localhost:8000/reports/sales_monthly');
        const data = await response.json();
        // Transform data to match chart format
        const transformed = data.map(item => ({
          month: `${item.year}-${item.month.toString().padStart(2, '0')}`,
          sales: item.total
        }));
        setSalesData(transformed);
      } catch (error) {
        console.error('Error fetching sales data:', error);
        // Fallback to mock data
        setSalesData([
          { month: 'Jan', sales: 12000 },
          { month: 'Feb', sales: 15000 },
          { month: 'Mar', sales: 18000 },
          { month: 'Apr', sales: 22000 },
          { month: 'May', sales: 25000 },
          { month: 'Jun', sales: 28000 },
        ]);
      }
    };
    fetchSalesData();
  }, []);

  const barData = {
    labels: salesData.map(d => d.month),
    datasets: [
      {
        label: 'Sales ($)',
        data: salesData.map(d => d.sales),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  const lineData = {
    labels: salesData.map(d => d.month),
    datasets: [
      {
        label: 'Sales Trend',
        data: salesData.map(d => d.sales),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
      },
    ],
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Sales Reports</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">Monthly Sales</h2>
          <Bar data={barData} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">Sales Trend</h2>
          <Line data={lineData} />
        </div>
      </div>
    </div>
  );
};

export default SalesReports;

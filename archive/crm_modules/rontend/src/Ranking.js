// frontend/src/Ranking.js
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const socket = io('http://localhost:3000');

function Ranking() {
    const [ranking, setRanking] = useState([]);

    useEffect(() => {
        // Recibir ranking en tiempo real
        socket.on('rankingUpdate', (data) => setRanking(data));
        return () => socket.off('rankingUpdate');
    }, []);

    const data = {
        labels: ranking.map(u => u.name),
        datasets: [
            {
                label: 'Puntos',
                data: ranking.map(u => u.points),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
                label: 'Ventas',
                data: ranking.map(u => u.sales),
                backgroundColor: 'rgba(153, 102, 255, 0.6)',
            }
        ]
    };

    return (
        <div style={{ width: '600px', margin: '20px auto' }}>
            <h3>Ranking y métricas comparativas</h3>
            <Bar data={data} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
            <ol>
                {ranking.map((u, i) => (
                    <li key={i}>{u.name} - {u.points} pts - {u.sales} ventas</li>
                ))}
            </ol>
        </div>
    );
}

export default Ranking;

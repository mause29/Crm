import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const socket = io('http://localhost:3000');

function Dashboard({ userId }) {
    const [user, setUser] = useState({});
    const [ranking, setRanking] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3000/api/ranking')
            .then(res => res.json())
            .then(data => setRanking(data));

        socket.on('rankingUpdate', (data) => setRanking(data));
        socket.on('userUpdate', (data) => {
            if(data._id === userId) setUser(data);
        });

        return () => {
            socket.off('rankingUpdate');
            socket.off('userUpdate');
        };
    }, [userId]);

    const chartData = {
        labels: ranking.map(u => u.name),
        datasets: [
            { label: 'Puntos', data: ranking.map(u => u.points), backgroundColor: 'rgba(75,192,192,0.6)' },
            { label: 'Ventas', data: ranking.map(u => u.sales), backgroundColor: 'rgba(153,102,255,0.6)' }
        ]
    };

    return (
        <div style={{ maxWidth: '900px', margin: '20px auto' }}>
            <h2>Dashboard Gamificación</h2>
            <div style={{ marginBottom: '20px' }}>
                <h3>Perfil de Usuario</h3>
                <p>Nombre: {user.name}</p>
                <p>Nivel: {user.level}</p>
                <p>Puntos: {user.points}</p>
                <p>Logros: {user.achievements?.join(', ')}</p>
                <p>Badges: {user.badges?.join(', ')}</p>
            </div>
            <div>
                <h3>Ranking y métricas comparativas</h3>
                <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
                <ol>
                    {ranking.map((u,i) => <li key={i}>{u.name} - {u.points} pts - {u.sales} ventas</li>)}
                </ol>
            </div>
        </div>
    );
}

export default Dashboard;

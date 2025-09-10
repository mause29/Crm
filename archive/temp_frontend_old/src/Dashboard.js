// frontend/src/Dashboard.js
import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';

function Dashboard() {
    const [data, setData] = useState({});

    useEffect(() => {
        fetch('http://localhost:3000/dashboard/stats')
        .then(res => res.json())
        .then(users => {
            setData({
                labels: users.map(u => u.name),
                datasets: [
                    { label: 'Points', data: users.map(u => u.points), backgroundColor: 'blue' },
                    { label: 'Level', data: users.map(u => u.level), backgroundColor: 'green' },
                    { label: 'Achievements', data: users.map(u => u.achievements), backgroundColor: 'orange' },
                ]
            });
        });
    }, []);

    return <Bar data={data} />;
}

export default Dashboard;

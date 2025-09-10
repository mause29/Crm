// frontend/src/Ranking.js
import { useEffect, useState } from 'react';

function Ranking() {
    const [ranking, setRanking] = useState([]);

    useEffect(() => {
        const fetchRanking = async () => {
            const res = await fetch('http://localhost:3000/gamification/ranking');
            const data = await res.json();
            setRanking(data);
        };
        fetchRanking();
        const interval = setInterval(fetchRanking, 5000); // Actualiza cada 5s
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h2>Ranking Top 10</h2>
            <ul>
                {ranking.map((user, i) => (
                    <li key={i}>
                        {i+1}. {user.name} - {user.points} pts - Nivel {user.level} - Badges: {user.achievements.join(', ')}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Ranking;

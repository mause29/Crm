// frontend/src/Profile.js
import { useEffect, useState } from 'react';

function Profile({ userId }) {
    const [user, setUser] = useState({ name: '', points: 0, level: 1, achievements: [] });

    useEffect(() => {
        const fetchUser = async () => {
            const res = await fetch(`http://localhost:3000/users/${userId}`);
            const data = await res.json();
            setUser(data);
        };
        fetchUser();
    }, [userId]);

    return (
        <div>
            <h2>{user.name}</h2>
            <p>Puntos: {user.points}</p>
            <p>Nivel: {user.level}</p>
            <h3>Logros y Badges:</h3>
            <ul>
                {user.achievements.map((a, i) => <li key={i}>{a}</li>)}
            </ul>
        </div>
    );
}

export default Profile;

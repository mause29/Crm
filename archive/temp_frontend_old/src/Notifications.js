// frontend/src/Notifications.js
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000');

function Notifications() {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        socket.on('notification', (data) => {
            setNotifications(prev => [data, ...prev]);
        });
        return () => socket.off('notification');
    }, []);

    return (
        <div style={{ position: 'fixed', top: 10, right: 10, width: 300 }}>
            {notifications.map((n, i) => (
                <div key={i} style={{ background: '#333', color: '#fff', padding: '10px', margin: '5px', borderRadius: '5px' }}>
                    {n.message}
                </div>
            ))}
        </div>
    );
}

export default Notifications;

// frontend/src/Notification.js
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000');

function Notification() {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        socket.on('receiveNotification', (data) => {
            setNotifications(prev => [...prev, data]);
        });
    }, []);

    return (
        <div className="notifications">
            {notifications.map((n, i) => (
                <div key={i} className="notification">{n.message}</div>
            ))}
        </div>
    );
}

export default Notification;

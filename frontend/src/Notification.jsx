import { useEffect, useState, useRef } from 'react';
import { io } from 'socket.io-client';

function Notification() {
    const [notifications, setNotifications] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [connectionError, setConnectionError] = useState(null);
    const [showAll, setShowAll] = useState(false);
    const socketRef = useRef(null);

    useEffect(() => {
        // Initialize Socket.IO connection
        const token = localStorage.getItem('token');
        const socketOptions = {
            transports: ['websocket', 'polling'],
            upgrade: true,
            rememberUpgrade: true,
            timeout: 20000,
            ...(token && {
                auth: { token: `Bearer ${token}` },
                extraHeaders: { Authorization: `Bearer ${token}` }
            })
        };

        socketRef.current = io('http://localhost:8000', socketOptions);

        // Connection event handlers
        socketRef.current.on('connect', () => {
            console.log('Connected to notification server');
            setIsConnected(true);
            setConnectionError(null);
        });

        socketRef.current.on('disconnect', (reason) => {
            console.log('Disconnected from notification server:', reason);
            setIsConnected(false);
            if (reason === 'io server disconnect') {
                setConnectionError('Server disconnected. Attempting to reconnect...');
            }
        });

        socketRef.current.on('connect_error', (error) => {
            console.error('Connection error:', error);
            setIsConnected(false);
            setConnectionError('Failed to connect to notification server');
        });

        socketRef.current.on('reconnect', (attemptNumber) => {
            console.log('Reconnected to notification server after', attemptNumber, 'attempts');
            setIsConnected(true);
            setConnectionError(null);
        });

        socketRef.current.on('reconnect_error', (error) => {
            console.error('Reconnection error:', error);
            setConnectionError('Failed to reconnect to notification server');
        });

        // Notification event handlers
        socketRef.current.on('receiveNotification', (data) => {
            console.log('Received notification:', data);
            const newNotification = {
                id: Date.now() + Math.random(),
                ...data,
                timestamp: new Date(),
                read: false,
                type: data.type || 'info'
            };
            setNotifications(prev => [newNotification, ...prev]);
        });

        socketRef.current.on('notification', (data) => {
            console.log('Received general notification:', data);
            const newNotification = {
                id: Date.now() + Math.random(),
                ...data,
                timestamp: new Date(),
                read: false,
                type: data.type || 'info'
            };
            setNotifications(prev => [newNotification, ...prev]);
        });

        // Cleanup on unmount
        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
            }
        };
    }, []);

    const markAsRead = (id) => {
        setNotifications(prev =>
            prev.map(notification =>
                notification.id === id
                    ? { ...notification, read: true }
                    : notification
            )
        );
    };

    const dismissNotification = (id) => {
        setNotifications(prev => prev.filter(notification => notification.id !== id));
    };

    const clearAllNotifications = () => {
        setNotifications([]);
    };

    const getNotificationIcon = (type) => {
        switch (type) {
            case 'success': return '✅';
            case 'warning': return '⚠️';
            case 'error': return '❌';
            case 'info':
            default: return 'ℹ️';
        }
    };

    const getNotificationColor = (type) => {
        switch (type) {
            case 'success': return 'border-green-200 bg-green-50';
            case 'warning': return 'border-yellow-200 bg-yellow-50';
            case 'error': return 'border-red-200 bg-red-50';
            case 'info':
            default: return 'border-blue-200 bg-blue-50';
        }
    };

    const unreadCount = notifications.filter(n => !n.read).length;
    const displayNotifications = showAll ? notifications : notifications.slice(0, 5);

    return (
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <div className="text-2xl mr-3">🔔</div>
                        <div>
                            <h3 className="text-lg font-semibold">Notificaciones</h3>
                            <div className="flex items-center text-sm">
                                <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
                                <span>{isConnected ? 'Conectado' : 'Desconectado'}</span>
                            </div>
                        </div>
                    </div>
                    {unreadCount > 0 && (
                        <div className="bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold">
                            {unreadCount}
                        </div>
                    )}
                </div>
            </div>

            {/* Connection Error */}
            {connectionError && (
                <div className="p-3 bg-red-50 border-l-4 border-red-400">
                    <div className="flex items-center">
                        <div className="text-red-400 mr-2">⚠️</div>
                        <p className="text-red-700 text-sm">{connectionError}</p>
                    </div>
                </div>
            )}

            {/* Notifications List */}
            <div className="max-h-96 overflow-y-auto">
                {notifications.length === 0 ? (
                    <div className="p-8 text-center">
                        <div className="text-gray-400 text-4xl mb-3">📭</div>
                        <p className="text-gray-500">No hay notificaciones</p>
                        <p className="text-gray-400 text-sm mt-1">Las nuevas notificaciones aparecerán aquí</p>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-100">
                        {displayNotifications.map((notification) => (
                            <div
                                key={notification.id}
                                className={`p-4 ${getNotificationColor(notification.type)} border-l-4 ${
                                    notification.type === 'success' ? 'border-green-400' :
                                    notification.type === 'warning' ? 'border-yellow-400' :
                                    notification.type === 'error' ? 'border-red-400' :
                                    'border-blue-400'
                                } ${!notification.read ? 'bg-opacity-75' : ''}`}
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-2">
                                            <span className="text-lg mr-2">
                                                {getNotificationIcon(notification.type)}
                                            </span>
                                            <span className="text-xs text-gray-500 uppercase font-medium">
                                                {notification.type}
                                            </span>
                                            {!notification.read && (
                                                <div className="w-2 h-2 bg-blue-500 rounded-full ml-2"></div>
                                            )}
                                        </div>
                                        <p className="text-gray-800 text-sm leading-relaxed">
                                            {notification.message || notification.title}
                                        </p>
                                        <div className="flex items-center justify-between mt-3">
                                            <span className="text-xs text-gray-500">
                                                {notification.timestamp.toLocaleTimeString()}
                                            </span>
                                            <div className="flex space-x-2">
                                                {!notification.read && (
                                                    <button
                                                        onClick={() => markAsRead(notification.id)}
                                                        className="text-xs text-blue-600 hover:text-blue-800 underline"
                                                    >
                                                        Marcar como leída
                                                    </button>
                                                )}
                                                <button
                                                    onClick={() => dismissNotification(notification.id)}
                                                    className="text-xs text-gray-500 hover:text-gray-700 underline"
                                                >
                                                    Descartar
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Footer */}
            {notifications.length > 5 && (
                <div className="p-3 bg-gray-50 border-t">
                    <button
                        onClick={() => setShowAll(!showAll)}
                        className="w-full text-sm text-blue-600 hover:text-blue-800 font-medium"
                    >
                        {showAll ? 'Mostrar menos' : `Mostrar todas (${notifications.length})`}
                    </button>
                </div>
            )}

            {notifications.length > 0 && (
                <div className="p-3 bg-gray-50 border-t">
                    <button
                        onClick={clearAllNotifications}
                        className="w-full text-sm text-red-600 hover:text-red-800 font-medium"
                    >
                        Limpiar todas las notificaciones
                    </button>
                </div>
            )}
        </div>
    );
}

export default Notification;

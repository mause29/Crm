import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setTheme } from './store';
import Dashboard from './components/Dashboard';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
    const theme = useSelector(state => state.user.theme);
    const dispatch = useDispatch();

    useEffect(() => {
        socket.on('receive_notification', msg => alert('Nueva notificación: ' + msg));
    }, []);

    return (
        <div className={theme === 'dark' ? 'bg-gray-900 text-white min-h-screen' : 'bg-white text-black min-h-screen'}>
            <header className="p-4 shadow flex justify-between">
                <h1 className="font-bold text-xl">CRM Avanzado</h1>
                <button onClick={() => dispatch(setTheme(theme === 'dark' ? 'light' : 'dark'))} className="px-4 py-2 bg-blue-500 rounded">Cambiar Tema</button>
            </header>
            <Dashboard socket={socket} />
        </div>
    );
}

export default App;

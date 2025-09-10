import Dashboard from './components/Dashboard';
import { UserProvider } from './context/UserContext';
import { useEffect } from 'react';
import { initShortcuts } from './utils/shortcuts';

function App() {
    useEffect(() => { initShortcuts(); }, []);

    return (
        <UserProvider>
            <Dashboard />
        </UserProvider>
    );
}

export default App;

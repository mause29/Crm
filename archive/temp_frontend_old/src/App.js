// frontend/src/App.js
import '../src/index.css';
import Ranking from './Ranking';
import Profile from './Profile';
import WeeklyChallenge from './WeeklyChallenge';
import Notifications from './Notifications';
import DealsPipeline from './DealsPipeline';
import Sidebar from './Sidebar';
import TopBar from './TopBar';

function App() {
    const userId = '64f...'; // ID del usuario conectado

    return (
        <div className="flex">
            <Sidebar />
            <div className="ml-16 flex-grow flex flex-col h-screen">
                <TopBar />
                <div className="flex-grow overflow-y-auto p-5">
                    <Notifications />
                    <Profile userId={userId} />
                    <WeeklyChallenge userId={userId} />
                    <Ranking />
                    <DealsPipeline />
                </div>
            </div>
        </div>
    );
}

export default App;

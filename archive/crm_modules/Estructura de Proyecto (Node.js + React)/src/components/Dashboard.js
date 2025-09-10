import ThemeSwitcher from './ThemeSwitcher';
import TaskBoard from './TaskBoard';

export default function Dashboard() {
    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Dashboard Personalizable</h1>
            <ThemeSwitcher />
            <TaskBoard />
        </div>
    );
}

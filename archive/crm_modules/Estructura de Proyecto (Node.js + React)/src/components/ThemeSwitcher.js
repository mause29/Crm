import { useContext } from 'react';
import { UserContext } from '../context/UserContext';

export default function ThemeSwitcher() {
    const { theme, toggleTheme } = useContext(UserContext);
    return (
        <button onClick={toggleTheme} className="px-4 py-2 rounded bg-blue-500 text-white">
            {theme === 'light' ? 'Modo Oscuro' : 'Modo Claro'}
        </button>
    );
}

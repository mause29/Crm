import React, { useState, useEffect } from 'react';

function WeeklyChallenge({ userId }) {
    const [points, setPoints] = useState(0);
    const [achievements, setAchievements] = useState([]);
    const [userAchievements, setUserAchievements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [completing, setCompleting] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        if (userId) {
            fetchAllData();
        }
    }, [userId]);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    };

    const fetchAllData = async () => {
        setLoading(true);
        setError(null);
        try {
            await Promise.all([
                fetchPoints(),
                fetchAchievements(),
                fetchUserAchievements()
            ]);
        } catch (err) {
            setError('Failed to load challenge data');
            console.error('Error fetching data:', err);
        } finally {
            setLoading(false);
        }
    };

    const fetchPoints = async () => {
        try {
            const response = await fetch(`http://localhost:8000/gamification/user_points/${userId}`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setPoints(data.total_points || 0);
        } catch (err) {
            console.error('Error fetching points:', err);
            throw err;
        }
    };

    const fetchAchievements = async () => {
        try {
            const response = await fetch('http://localhost:8000/gamification/achievements', {
                headers: getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setAchievements(data || []);
        } catch (err) {
            console.error('Error fetching achievements:', err);
            throw err;
        }
    };

    const fetchUserAchievements = async () => {
        try {
            const response = await fetch(`http://localhost:8000/gamification/user_achievements/${userId}`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setUserAchievements(data || []);
        } catch (err) {
            console.error('Error fetching user achievements:', err);
            throw err;
        }
    };

    const completeChallenge = async () => {
        if (completing) return;

        setCompleting(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/gamification/complete_challenge', {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ user_id: userId })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            setSuccessMessage('🎉 ¡Reto completado! Puntos añadidos a tu cuenta.');
            setTimeout(() => setSuccessMessage(''), 5000);

            // Refresh data
            await fetchPoints();
            await fetchUserAchievements();

        } catch (err) {
            setError('Error al completar el reto. Inténtalo de nuevo.');
            console.error('Error completing challenge:', err);
        } finally {
            setCompleting(false);
        }
    };

    if (loading) {
        return (
            <div className="p-6 bg-white rounded-lg shadow-md">
                <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                    <span className="ml-3 text-gray-600">Cargando reto semanal...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-6 bg-white rounded-lg shadow-md">
                <div className="text-center py-8">
                    <div className="text-red-500 text-4xl mb-4">⚠️</div>
                    <h3 className="text-lg font-semibold text-red-800 mb-2">Error al Cargar Datos</h3>
                    <p className="text-red-600 mb-4">{error}</p>
                    <button
                        onClick={fetchAllData}
                        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
                    >
                        Intentar de Nuevo
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            {/* Success Message */}
            {successMessage && (
                <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center">
                        <div className="text-green-500 mr-3">✅</div>
                        <p className="text-green-800">{successMessage}</p>
                    </div>
                </div>
            )}

            {/* Header */}
            <div className="mb-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-2">🏆 Reto Semanal</h3>
                <p className="text-gray-600">Completa tu objetivo de ventas o tickets para ganar puntos!</p>
            </div>

            {/* Points Display */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-lg mb-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h4 className="text-lg font-semibold">Puntos Totales</h4>
                        <p className="text-blue-100">Tu progreso actual</p>
                    </div>
                    <div className="text-3xl font-bold">{points.toLocaleString()}</div>
                </div>
            </div>

            {/* Complete Challenge Button */}
            <div className="mb-8">
                <button
                    onClick={completeChallenge}
                    disabled={completing}
                    className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-colors ${
                        completing
                            ? 'bg-gray-400 cursor-not-allowed'
                            : 'bg-green-500 hover:bg-green-600 active:bg-green-700'
                    }`}
                >
                    {completing ? (
                        <div className="flex items-center justify-center">
                            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                            Completando...
                        </div>
                    ) : (
                        '🎯 Completar Reto Semanal'
                    )}
                </button>
            </div>

            {/* Achievements Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Available Achievements */}
                <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                        <span className="mr-2">🎖️</span>
                        Logros Disponibles
                    </h4>
                    {achievements.length > 0 ? (
                        <div className="space-y-3">
                            {achievements.map(achievement => {
                                const isUnlocked = userAchievements.some(ua => ua.achievement_id === achievement.id);
                                return (
                                    <div
                                        key={achievement.id}
                                        className={`p-3 rounded-lg border ${
                                            isUnlocked
                                                ? 'bg-green-50 border-green-200'
                                                : 'bg-white border-gray-200'
                                        }`}
                                    >
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <h5 className={`font-medium ${isUnlocked ? 'text-green-800' : 'text-gray-800'}`}>
                                                    {achievement.name}
                                                    {isUnlocked && <span className="ml-2 text-green-600">✓</span>}
                                                </h5>
                                                <p className="text-sm text-gray-600 mt-1">{achievement.description}</p>
                                            </div>
                                            <div className="text-right ml-3">
                                                <div className={`text-sm font-medium ${
                                                    isUnlocked ? 'text-green-600' : 'text-blue-600'
                                                }`}>
                                                    {achievement.points_required} pts
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <p className="text-gray-500 text-sm">No hay logros disponibles en este momento.</p>
                    )}
                </div>

                {/* User's Achievements */}
                <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                        <span className="mr-2">🏅</span>
                        Tus Logros
                    </h4>
                    {userAchievements.length > 0 ? (
                        <div className="space-y-2">
                            {userAchievements.map(ua => {
                                const achievement = achievements.find(a => a.id === ua.achievement_id);
                                return (
                                    <div key={ua.id} className="flex items-center p-2 bg-white rounded border">
                                        <div className="text-green-500 mr-3">🏆</div>
                                        <div>
                                            <div className="font-medium text-gray-800">
                                                {achievement ? achievement.name : 'Logro desconocido'}
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                Desbloqueado: {new Date(ua.unlocked_at).toLocaleDateString()}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-4">
                            <div className="text-gray-400 text-3xl mb-2">🎯</div>
                            <p className="text-gray-500 text-sm">Aún no has desbloqueado ningún logro.</p>
                            <p className="text-gray-400 text-xs mt-1">¡Completa retos para ganar logros!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default WeeklyChallenge;

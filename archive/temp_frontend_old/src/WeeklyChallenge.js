// frontend/src/WeeklyChallenge.js
function WeeklyChallenge({ userId }) {
    const completeChallenge = async () => {
        await fetch('http://localhost:3000/gamification/completeChallenge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId })
        });
        alert('Reto completado y puntos añadidos!');
    };

    return (
        <div>
            <h3>Reto Semanal</h3>
            <p>Completa tu objetivo de ventas o tickets!</p>
            <button onClick={completeChallenge}>Completar Reto</button>
        </div>
    );
}

export default WeeklyChallenge;

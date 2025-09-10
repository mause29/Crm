export function initShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'n') {
            alert('Nuevo registro!');
        }
        if (e.ctrlKey && e.key === 'd') {
            alert('Ir al dashboard!');
        }
    });
}

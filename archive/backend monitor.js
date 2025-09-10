// backend/monitor.js
const axios = require('axios');

async function checkUptime(url) {
    try {
        const res = await axios.get(url);
        console.log(`${url} está online. Status: ${res.status}`);
    } catch (err) {
        console.error(`${url} está caído!`);
        // Aquí enviar alerta (email, webhook, etc.)
    }
}

setInterval(() => checkUptime('https://mi-crm.com'), 60000); // cada minuto

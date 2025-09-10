// biIntegration.js
const axios = require('axios');

// Power BI o Tableau
async function sendDataToBI(dataset, biPlatform) {
    let url = biPlatform === 'powerbi' ? 'https://api.powerbi.com/datasets' : 'https://tableau.com/api/datasets';
    await axios.post(url, dataset);
}

// Webhook genérico
async function triggerWebhook(url, payload) {
    await axios.post(url, payload);
}

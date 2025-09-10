const axios = require('axios');
const { bi } = require('../config');

async function sendDataToBI(dataset, platform){
    const url = platform === 'powerbi' ? bi.powerbiUrl : bi.tableauUrl;
    await axios.post(url, dataset);
}

async function triggerWebhook(url, payload){
    await axios.post(url, payload);
}

module.exports = { sendDataToBI, triggerWebhook };

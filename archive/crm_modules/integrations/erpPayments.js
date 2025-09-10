const axios = require('axios');
const { erp, payments } = require('../config');

async function syncERP(order){
    await axios.post(`${erp.url}/orders`, order);
}

async function processPayment(paymentInfo, platform){
    const urls = { stripe: payments.stripeUrl, paypal: payments.paypalUrl, mercadoPago: payments.mercadoPagoUrl };
    return await axios.post(urls[platform], paymentInfo);
}

module.exports = { syncERP, processPayment };

// erpIntegration.js
const axios = require('axios');

// Sincronización de facturación y stock
async function syncERP(order) {
    await axios.post('https://api.erp.com/orders', order);
}

// Pagos adicionales
async function processPayment(paymentInfo, platform) {
    let url;
    switch(platform) {
        case 'stripe': url = 'https://api.stripe.com/v1/charges'; break;
        case 'paypal': url = 'https://api.paypal.com/v1/payments/payment'; break;
        case 'mercadopago': url = 'https://api.mercadopago.com/v1/payments'; break;
    }
    return await axios.post(url, paymentInfo);
}

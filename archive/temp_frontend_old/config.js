module.exports = {
    email: {
        host: 'smtp.tuservidor.com',
        port: 587,
        user: 'no-reply@tusistema.com',
        pass: 'tucontraseña'
    },
    social: {
        facebookToken: 'TOKEN_FACEBOOK',
        instagramToken: 'TOKEN_INSTAGRAM'
    },
    erp: { url: 'https://api.erp.com' },
    payments: {
        stripeUrl: 'https://api.stripe.com/v1/charges',
        paypalUrl: 'https://api.paypal.com/v1/payments/payment',
        mercadoPagoUrl: 'https://api.mercadopago.com/v1/payments'
    },
    bi: {
        powerbiUrl: 'https://api.powerbi.com/datasets',
        tableauUrl: 'https://tableau.com/api/datasets'
    },
    webhooks: {}
};

// server/billing.js
const paypal = require('@paypal/checkout-server-sdk');

const environment = new paypal.core.SandboxEnvironment(process.env.PAYPAL_CLIENT, process.env.PAYPAL_SECRET);
const client = new paypal.core.PayPalHttpClient(environment);

async function createInvoice(invoiceData) {
  const request = new paypal.invoices.InvoicesCreateRequest();
  request.requestBody(invoiceData);
  return await client.execute(request);
}

// Pago con tarjeta sin cuenta PayPal
async function capturePayment(orderId) {
  const request = new paypal.orders.OrdersCaptureRequest(orderId);
  request.requestBody({});
  return await client.execute(request);
}

module.exports = { createInvoice, capturePayment };

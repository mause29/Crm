// server/ml.js
const tf = require('@tensorflow/tfjs-node');
const clientModel = require('./models/client'); // MongoDB Mongoose

// --- Predicción de cierre de oportunidades ---
async function predictOpportunity(opportunity) {
  // Dummy modelo simple: 0-100% de cierre
  const chance = Math.min(100, (opportunity.value / 10000) * 100);
  return chance;
}

// --- Segmentación automática ---
async function segmentClients() {
  const clients = await clientModel.find();
  return clients.map(c => {
    if (c.totalSpent > 10000) return { ...c._doc, segment: 'VIP' };
    if (c.lastPurchase > 180) return { ...c._doc, segment: 'Riesgo' };
    return { ...c._doc, segment: 'Normal' };
  });
}

// --- Detección de clientes inactivos ---
async function detectInactiveClients() {
  const clients = await clientModel.find();
  return clients.filter(c => {
    const last = new Date(c.lastPurchase);
    const now = new Date();
    return (now - last) / (1000 * 60 * 60 * 24) > 90;
  });
}

module.exports = { predictOpportunity, segmentClients, detectInactiveClients };

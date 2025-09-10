// server/reporting.js
const clientModel = require('./models/client');
const opportunityModel = require('./models/opportunity');

async function salesByPeriod(start, end) {
  return await opportunityModel.aggregate([
    { $match: { createdAt: { $gte: start, $lte: end } } },
    { $group: { _id: null, total: { $sum: "$value" } } }
  ]);
}

async function topClients() {
  return await clientModel.aggregate([
    { $sort: { totalSpent: -1 } },
    { $limit: 10 }
  ]);
}

async function alertLowSales(threshold) {
  const total = await salesByPeriod(new Date(new Date().setDate(new Date().getDate()-30)), new Date());
  if (total[0].total < threshold) return true;
  return false;
}

module.exports = { salesByPeriod, topClients, alertLowSales };

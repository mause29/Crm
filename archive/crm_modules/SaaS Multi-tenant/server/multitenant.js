// server/multitenant.js
const mongoose = require('mongoose');

// Conexión a base de datos por empresa
function connectTenantDb(companyId) {
  const uri = `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster.mongodb.net/${companyId}?retryWrites=true&w=majority`;
  return mongoose.createConnection(uri, { useNewUrlParser: true, useUnifiedTopology: true });
}

module.exports = { connectTenantDb };

// server/automation.js
const { sendWhatsAppMessage } = require('./integrations');
const clientModel = require('./models/client');
const taskModel = require('./models/task');

async function followUpInactiveClients() {
  const inactive = await clientModel.find({ lastPurchase: { $lt: new Date(Date.now()-90*24*60*60*1000) } });
  for (const client of inactive) {
    await sendWhatsAppMessage(client.phone, `Hola ${client.name}, te extrañamos!`);
  }
}

async function autoAssignTasks() {
  const tasks = await taskModel.find({ assignedTo: null });
  for (const task of tasks) {
    task.assignedTo = await getAvailableUser();
    await task.save();
  }
}

async function getAvailableUser() {
  // Dummy: devuelve usuario aleatorio
  return 'user123';
}

// Integración con Zapier o Integromat se hace vía webhook
async function triggerWebhook(url, data) {
  const axios = require('axios');
  await axios.post(url, data);
}

module.exports = { followUpInactiveClients, autoAssignTasks, triggerWebhook };

const { triggerWebhook } = require('../integrations/biWebhooks');
const tasks = require('../models/tasks');
const leads = require('../models/leads');
const { sendReminderEmail } = require('./emailsReminders');
const logger = require('../utils/logger');

// Escalado automático de tareas críticas
async function escalateCriticalTasks() {
    const criticalTasks = await tasks.getPendingCritical();
    for(const task of criticalTasks){
        logger.info(`Escalando tarea crítica: ${task.title}`);
        await triggerWebhook('https://mi-sistema.com/webhook/tasks', task);
    }
}

// Ruteo automático de leads
async function routeLeads() {
    const unassignedLeads = await leads.getUnassigned();
    const teamPerformance = await leads.getTeamPerformance();

    for(const lead of unassignedLeads){
        const bestAgent = teamPerformance.sort((a,b)=>b.score-a.score)[0];
        await leads.assignLead(lead.id, bestAgent.id);
        logger.info(`Lead ${lead.id} asignado a ${bestAgent.name}`);
    }
}

// Reactivación de oportunidades frías
async function reactivateColdLeads() {
    const coldLeads = await leads.getColdLeads();
    for(const lead of coldLeads){
        await sendReminderEmail(lead.owner, { title: 'Oportunidad fría', dueDate: new Date() });
        logger.info(`Reactivación enviada a ${lead.email}`);
    }
}

module.exports = {
    escalateCriticalTasks,
    routeLeads,
    reactivateColdLeads
};

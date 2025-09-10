// automation.js
const axios = require('axios');
const tasks = require('./tasks'); // tu módulo de tareas
const leads = require('./leads'); // tu módulo de leads

// Escalado automático de tareas críticas no completadas
async function escalateCriticalTasks() {
    const criticalTasks = await tasks.getPendingCritical();
    criticalTasks.forEach(task => {
        // Notificar a supervisores
        axios.post('https://api.tusistema.com/notify', {
            message: `Tarea crítica pendiente: ${task.title}`,
            userId: task.owner
        });
    });
}

// Ruteo automático de leads según desempeño del equipo
async function routeLeads() {
    const unassignedLeads = await leads.getUnassigned();
    const teamPerformance = await leads.getTeamPerformance();

    unassignedLeads.forEach(lead => {
        const bestAgent = teamPerformance.sort((a,b)=>b.score-a.score)[0];
        leads.assignLead(lead.id, bestAgent.id);
    });
}

// Reactivación de oportunidades frías
async function reactivateColdLeads() {
    const coldLeads = await leads.getColdLeads();
    coldLeads.forEach(lead => {
        axios.post('https://api.tusistema.com/send_email', {
            email: lead.email,
            template: 'reactivation'
        });
    });
}

// Scheduler
setInterval(() => {
    escalateCriticalTasks();
    routeLeads();
    reactivateColdLeads();
}, 1000*60*5); // cada 5 minutos

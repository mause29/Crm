const { escalateCriticalTasks, routeLeads, reactivateColdLeads } = require('./workflows/tasksAutomation');
const { sendReminderEmail } = require('./workflows/emailsReminders');
const { postToFacebook, postToInstagram } = require('./integrations/social');
const logger = require('./utils/logger');

async function mainWorkflow() {
    try {
        await escalateCriticalTasks();
        await routeLeads();
        await reactivateColdLeads();

        // Ejemplo de post automático en redes sociales
        await postToFacebook("Actualización diaria de leads y tareas");
        await postToInstagram("Imagen de resumen diario");

        logger.info("Workflow ejecutado correctamente");
    } catch(err) {
        logger.error("Error en workflow:", err);
    }
}

// Scheduler cada 5 minutos
setInterval(mainWorkflow, 1000*60*5);

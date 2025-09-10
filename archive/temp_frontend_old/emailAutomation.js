// emailAutomation.js
const nodemailer = require('nodemailer');
const calendar = require('./calendar'); // integración con Google/Outlook

async function sendReminderEmail(user, task) {
    let transporter = nodemailer.createTransport({
        host: "smtp.tuservidor.com",
        port: 587,
        auth: { user: "tuemail", pass: "tucontraseña" }
    });

    await transporter.sendMail({
        from: '"Sistema CRM" <no-reply@tusistema.com>',
        to: user.email,
        subject: `Recordatorio: ${task.title}`,
        text: `Hola ${user.name}, recuerda completar la tarea: ${task.title} antes de ${task.dueDate}.`
    });
}

// Ejemplo de workflow configurable
async function workflowAutomation() {
    const tasksDueToday = await tasks.getDueToday();
    tasksDueToday.forEach(task => sendReminderEmail(task.owner, task));
}

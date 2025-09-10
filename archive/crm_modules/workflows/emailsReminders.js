const nodemailer = require('nodemailer');
const { email: emailConfig } = require('../config');

const transporter = nodemailer.createTransport({
    host: emailConfig.host,
    port: emailConfig.port,
    auth: { user: emailConfig.user, pass: emailConfig.pass }
});

async function sendReminderEmail(user, task) {
    await transporter.sendMail({
        from: `"CRM System" <${emailConfig.user}>`,
        to: user.email,
        subject: `Recordatorio: ${task.title}`,
        text: `Hola ${user.name}, recuerda: ${task.title} antes del ${task.dueDate}`
    });
}

module.exports = { sendReminderEmail };

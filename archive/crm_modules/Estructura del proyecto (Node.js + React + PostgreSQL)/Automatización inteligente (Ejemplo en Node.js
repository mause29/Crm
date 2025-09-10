const { sendNotification } = require('../services/push');

async function autoEscalateTasks() {
  const overdueTasks = await Task.findAll({ where: { status: 'pending', dueDate: { $lt: new Date() } } });
  overdueTasks.forEach(async task => {
    task.status = 'escalated';
    await task.save();
    sendNotification(task.assignedTo, `La tarea ${task.title} ha sido escalada automáticamente.`);
  });
}

setInterval(autoEscalateTasks, 1000 * 60 * 5); // Revisa cada 5 minutos

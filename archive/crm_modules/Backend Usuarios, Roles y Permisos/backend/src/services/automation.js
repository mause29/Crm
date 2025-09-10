// backend/src/services/automation.js
import { unlockAchievement } from './gamification.js';
import { sendRealtimeNotification, sendEmail } from './notifications.js';
import { updateUserLevel } from './levels.js';

export async function newLeadAutomation(lead) {
  // Gamificación
  await unlockAchievement(lead.userId, 'Primer Lead Capturado');

  // Actualiza nivel
  const level = await updateUserLevel(lead.userId);

  // Notificaciones en tiempo real
  sendRealtimeNotification(lead.userId, `¡Has subido al nivel ${level}!`);
  sendEmail(lead.userEmail, 'Nuevo Nivel Alcanzado', `Felicidades, ahora eres nivel ${level}`);
}

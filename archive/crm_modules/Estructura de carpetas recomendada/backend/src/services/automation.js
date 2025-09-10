// backend/src/services/automation.js
import { unlockAchievement } from './gamification.js';
import { sendLeadToExternalCRM } from './integrations.js';

export async function newLeadAutomation(lead) {
  // Desbloquear logro por primer lead
  await unlockAchievement(lead.userId, 'Primer Lead Capturado');

  // Enviar lead al CRM externo automáticamente
  await sendLeadToExternalCRM(lead);
}

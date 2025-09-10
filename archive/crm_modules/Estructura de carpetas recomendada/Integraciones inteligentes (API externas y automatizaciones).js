// backend/src/services/integrations.js
import axios from 'axios';

// Ejemplo: integración con CRM externo o ERP
export async function sendLeadToExternalCRM(lead) {
  try {
    const response = await axios.post('https://external-crm.com/api/leads', lead, {
      headers: { Authorization: `Bearer ${process.env.CRM_API_KEY}` },
    });
    return response.data;
  } catch (err) {
    console.error('Error al enviar lead', err);
    return null;
  }
}

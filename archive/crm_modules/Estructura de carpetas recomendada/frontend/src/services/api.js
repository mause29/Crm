// frontend/src/services/api.js
import axios from 'axios';

export async function getDashboardData() {
  const res = await axios.get('/api/crm/dashboard');
  return res.data;
}

export async function submitNewLead(lead) {
  const res = await axios.post('/api/crm/leads', lead);
  return res.data;
}

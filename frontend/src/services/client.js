import api from './api.js';

class ClientService {
  async createClient(clientData) {
    const formData = new FormData();
    formData.append('name', clientData.name);
    formData.append('email', clientData.email);
    formData.append('phone', clientData.phone);

    const response = await fetch(`${api.baseURL}/clients/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to create client');
    }

    return response.json();
  }

  async getClients() {
    return api.get('/clients/');
  }

  async getClient(id) {
    return api.get(`/clients/${id}`);
  }

  async updateClient(id, clientData) {
    return api.put(`/clients/${id}`, clientData);
  }

  async deleteClient(id) {
    return api.delete(`/clients/${id}`);
  }
}

export default new ClientService();

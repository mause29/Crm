import api from './api.js';

class OpportunityService {
  async createOpportunity(opportunityData) {
    return api.post('/opportunities/', opportunityData);
  }

  async getOpportunities() {
    return api.get('/opportunities/');
  }

  async getOpportunity(id) {
    return api.get(`/opportunities/${id}`);
  }

  async updateOpportunity(id, opportunityData) {
    return api.put(`/opportunities/${id}`, opportunityData);
  }

  async deleteOpportunity(id) {
    return api.delete(`/opportunities/${id}`);
  }
}

export default new OpportunityService();

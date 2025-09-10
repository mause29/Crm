import api from './api.js';

class UserService {
  async createUser(userData) {
    return api.post('/users/', userData);
  }

  async getUsers() {
    return api.get('/users/');
  }

  async getUser(id) {
    return api.get(`/users/${id}`);
  }

  async updateUser(id, userData) {
    return api.put(`/users/${id}`, userData);
  }

  async deleteUser(id) {
    return api.delete(`/users/${id}`);
  }
}

export default new UserService();

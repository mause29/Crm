import api from './api.js';

class NotificationService {
  async getNotifications(userId) {
    return api.get(`/notifications/?user_id=${userId}`);
  }

  async createNotification(notificationData) {
    return api.post('/notifications/', notificationData);
  }

  async deleteNotification(id) {
    return api.delete(`/notifications/${id}`);
  }
}

export default new NotificationService();

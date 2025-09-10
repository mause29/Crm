import api from './api.js';

class InvoiceService {
  async createInvoice(invoiceData) {
    return api.post('/invoices/', invoiceData);
  }

  async getInvoices() {
    return api.get('/invoices/');
  }

  async getInvoice(id) {
    return api.get(`/invoices/${id}`);
  }

  async updateInvoice(id, invoiceData) {
    return api.put(`/invoices/${id}`, invoiceData);
  }

  async deleteInvoice(id) {
    return api.delete(`/invoices/${id}`);
  }
}

export default new InvoiceService();

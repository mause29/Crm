import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const getClients = () => api.get("/clients");
export const createInvoice = (amount) => api.post("/invoices/create-order", { amount });
export const captureInvoice = (orderId) => api.post(`/invoices/capture-order/${orderId}`);

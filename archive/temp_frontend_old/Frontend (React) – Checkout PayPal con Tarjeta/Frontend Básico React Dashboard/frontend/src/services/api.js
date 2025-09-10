import axios from 'axios';

const API_URL = "http://localhost:5000";

export const login = (email, password) => axios.post(`${API_URL}/auth/login`, { email, password });
export const getClients = (token) => axios.get(`${API_URL}/clients`, { headers: { Authorization: `Bearer ${token}` } });

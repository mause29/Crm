// backend/src/services/notifications.js
import nodemailer from 'nodemailer';
import { io } from '../index.js'; // instancia de Socket.IO

export function sendRealtimeNotification(userId, message) {
  io.to(`user_${userId}`).emit('notification', { message });
}

export async function sendEmail(to, subject, text) {
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASS },
  });
  await transporter.sendMail({ from: process.env.EMAIL_USER, to, subject, text });
}

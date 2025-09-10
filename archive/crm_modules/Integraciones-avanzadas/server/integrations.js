// server/integrations.js
const { google } = require('googleapis');
const axios = require('axios');

// --- Google Calendar ---
async function addEventToGoogleCalendar(auth, event) {
  const calendar = google.calendar({ version: 'v3', auth });
  return await calendar.events.insert({ calendarId: 'primary', requestBody: event });
}

// --- WhatsApp Business API (Ejemplo Twilio) ---
async function sendWhatsAppMessage(to, message) {
  const accountSid = process.env.TWILIO_SID;
  const authToken = process.env.TWILIO_TOKEN;
  const client = require('twilio')(accountSid, authToken);
  return await client.messages.create({
    from: 'whatsapp:' + process.env.TWILIO_WHATSAPP_FROM,
    to: 'whatsapp:' + to,
    body: message
  });
}

// --- Telefonía VoIP (Ejemplo Twilio) ---
async function makeCall(to, from, url) {
  const client = require('twilio')(process.env.TWILIO_SID, process.env.TWILIO_TOKEN);
  return await client.calls.create({ to, from, url });
}

module.exports = { addEventToGoogleCalendar, sendWhatsAppMessage, makeCall };

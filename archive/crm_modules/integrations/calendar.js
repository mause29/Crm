// calendar.js
const { google } = require('googleapis');

async function addEventGoogle(userToken, event) {
    const calendar = google.calendar({ version: 'v3', auth: userToken });
    await calendar.events.insert({ calendarId: 'primary', resource: event });
}

module.exports = { addEventGoogle };

// social.js
const axios = require('axios');
const { social } = require('../config');

async function postToFacebook(message){
    await axios.post(`https://graph.facebook.com/me/feed?access_token=${social.facebookToken}`, { message });
}

async function postToInstagram(message){
    await axios.post(`https://graph.instagram.com/me/media?access_token=${social.instagramToken}`, {
        caption: message,
        media_type: "IMAGE",
        image_url: "https://tuservidor.com/imagen.jpg"
    });
}

module.exports = { postToFacebook, postToInstagram };

// socialIntegration.js
const axios = require('axios');

async function postToFacebook(pageToken, message) {
    await axios.post(`https://graph.facebook.com/me/feed?access_token=${pageToken}`, { message });
}

async function postToInstagram(accessToken, message) {
    await axios.post(`https://graph.instagram.com/me/media?access_token=${accessToken}`, {
        caption: message,
        media_type: "IMAGE",
        image_url: "https://tuservidor.com/imagen.jpg"
    });
}

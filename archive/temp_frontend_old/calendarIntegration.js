// calendarIntegration.js
const { google } = require('googleapis');
const outlook = require('node-outlook');

async function addEventGoogle(userToken, event) {
    const calendar = google.calendar({ version: 'v3', auth: userToken });
    await calendar.events.insert({
        calendarId: 'primary',
        resource: event
    });
}

async function addEventOutlook(accessToken, event) {
    await outlook.calendar.createEvent({ accessToken, event });
}

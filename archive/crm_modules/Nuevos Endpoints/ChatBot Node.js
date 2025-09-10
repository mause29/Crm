// server.js (agregar después de endpoints previos)
const { processMessage } = require('./ai_chatbot');

app.post('/api/chatbot', async (req, res) => {
    const { clientMessage, clientId } = req.body;
    try {
        const response = await processMessage(clientMessage, clientId);
        res.json({ reply: response });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

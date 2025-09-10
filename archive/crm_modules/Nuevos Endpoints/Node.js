// server.js (agregar después de los endpoints anteriores)
const { routeLead, generateAlerts } = require('./ai_automation');

// Endpoint para ruteo inteligente de leads
app.post('/api/route-lead', async (req, res) => {
    const { leadData } = req.body;
    try {
        const assignedAgent = await routeLead(leadData);
        res.json({ assignedAgent });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para generar alertas automáticas
app.post('/api/alerts', async (req, res) => {
    const { dataStream } = req.body; // puede ser historial de ventas, tickets o clientes
    try {
        const alerts = await generateAlerts(dataStream);
        res.json({ alerts });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

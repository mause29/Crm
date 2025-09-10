// server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { analyzeSentiment, predictLeadClosure, recommendUpsell } = require('./ai');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Endpoint para análisis de sentimiento
app.post('/api/sentiment', async (req, res) => {
    const { message } = req.body;
    try {
        const sentiment = await analyzeSentiment(message);
        res.json({ sentiment });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para predicción de cierre de lead
app.post('/api/predict-lead', async (req, res) => {
    const { leadData } = req.body;
    try {
        const probability = await predictLeadClosure(leadData);
        res.json({ probability });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para recomendaciones de upsell/cross-sell
app.post('/api/recommend', async (req, res) => {
    const { customerData } = req.body;
    try {
        const recommendations = await recommendUpsell(customerData);
        res.json({ recommendations });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

const PORT = 5000;
app.listen(PORT, () => console.log(`IA CRM API corriendo en puerto ${PORT}`));

// microservices/ai/app.js
import express from 'express';
import bodyParser from 'body-parser';
import { predictChurn, sentimentAnalysis } from './services/aiService.js';

const app = express();
app.use(bodyParser.json());

app.post('/predict-churn', async (req, res) => {
  const result = await predictChurn(req.body);
  res.json(result);
});

app.post('/sentiment', async (req, res) => {
  const sentiment = await sentimentAnalysis(req.body.message);
  res.json({ sentiment });
});

app.listen(5000, () => console.log('Microservicio AI corriendo en puerto 5000'));

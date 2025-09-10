// backend/src/app.js
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import session from 'express-session';
import authRoutes from './routes/auth.js';
import crmRoutes from './routes/crm.js';
import notificationService from './services/notifications.js';

const app = express();

// Middlewares de seguridad
app.use(cors());
app.use(helmet());
app.use(express.json());
app.use(rateLimit({ windowMs: 1 * 60 * 1000, max: 100 }));

// Sesión
app.use(session({ secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: true }));

// Rutas
app.use('/api/auth', authRoutes);
app.use('/api/crm', crmRoutes);

// Notificaciones en tiempo real (WebSocket)
notificationService(app);

app.listen(process.env.PORT || 3000, () => console.log('CRM backend corriendo'));

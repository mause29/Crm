const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const session = require('express-session');
const authRoutes = require('./routes/auth');
const clientsRoutes = require('./routes/clients');
const tasksRoutes = require('./routes/tasks');
const invoicesRoutes = require('./routes/invoices');
const analyticsRoutes = require('./routes/analytics');
const { auditLogger, securityMiddleware } = require('./middleware/security');

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(session({ secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: true }));

// Middleware de seguridad y auditoría
app.use(securityMiddleware);
app.use(auditLogger);

// Rutas principales
app.use('/api/auth', authRoutes);
app.use('/api/clients', clientsRoutes);
app.use('/api/tasks', tasksRoutes);
app.use('/api/invoices', invoicesRoutes);
app.use('/api/analytics', analyticsRoutes);

app.listen(process.env.PORT || 5000, () => console.log(`Server running on port ${process.env.PORT || 5000}`));

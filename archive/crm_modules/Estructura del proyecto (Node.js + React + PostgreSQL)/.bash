crm-project/
│
├── backend/
│   ├── app.js              # Servidor principal Node.js/Express
│   ├── routes/
│   │   ├── auth.js         # Autenticación, 2FA, biometría
│   │   ├── clients.js      # Gestión de clientes
│   │   ├── tasks.js        # Gestión de tareas y pipelines
│   │   ├── invoices.js     # Facturación y suscripciones
│   │   └── analytics.js    # KPIs, análisis predictivo
│   ├── controllers/
│   ├── models/             # Modelos Sequelize/PostgreSQL
│   ├── middleware/
│   │   ├── auth.js         # JWT, permisos
│   │   ├── auditLog.js     # Logs de auditoría
│   │   └── security.js     # CSRF, XSS, inyecciones
│   └── services/
│       ├── email.js        # Notificaciones email
│       ├── sms.js          # Notificaciones SMS
│       ├── push.js         # Push web
│       └── ai.js           # IA para NLP, upsell, análisis de sentimiento
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── KanbanBoard.jsx
│   │   │   ├── Calendar.jsx
│   │   │   ├── Notifications.jsx
│   │   │   └── Leaderboard.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Clients.jsx
│   │   │   ├── Tasks.jsx
│   │   │   ├── Invoices.jsx
│   │   │   └── Analytics.jsx
│   │   ├── services/
│   │   │   ├── api.js        # Axios para comunicación con backend
│   │   │   ├── authService.js
│   │   │   └── aiService.js
│   │   └── styles/
│   │       ├── darkTheme.css
│   │       └── lightTheme.css
│   └── package.json
│
├── docker-compose.yml      # Contenedores backend, frontend, DB
├── .env                    # Variables de entorno
└── README.md

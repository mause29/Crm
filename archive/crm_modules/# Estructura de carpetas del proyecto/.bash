# Estructura de carpetas del proyecto
crm_project/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ database.py
│  │  ├─ auth.py
│  │  ├─ security.py
│  │  ├─ routes/
│  │  │  ├─ users.py
│  │  │  ├─ clients.py
│  │  │  ├─ opportunities.py
│  │  │  ├─ invoices.py
│  │  │  ├─ reports.py
│  │  │  ├─ analytics.py
│  │  │  ├─ notifications.py
│  │  │  ├─ integrations.py
│  │  │  └─ gamification.py
│  ├─ requirements.txt
├─ frontend/
│  ├─ src/
│  │  ├─ App.jsx
│  │  ├─ index.jsx
│  │  ├─ components/
│  │  │  ├─ Dashboard.jsx
│  │  │  ├─ Clients.jsx
│  │  │  ├─ Opportunities.jsx
│  │  │  ├─ Invoices.jsx
│  │  │  ├─ Reports.jsx
│  │  │  ├─ Analytics.jsx
│  │  │  ├─ Notifications.jsx
│  │  │  └─ Gamification.jsx
│  │  └─ services/
│  │     └─ api.js
├─ docker-compose.yml
└─ README.md

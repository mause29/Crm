import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login.jsx';
import Layout from './Layout.jsx';
import DealsPipeline from './DealsPipeline.jsx';
import CRMFormsTable from './CRMFormsTable.jsx';
import Notifications from './Notifications.jsx';
import Profile from './Profile.jsx';
import Dashboard from './Dashboard.jsx';
import ReportsDashboard from './ReportsDashboard.jsx';
import TaskManager from './TaskManager.jsx';
import EmailManager from './EmailManager.jsx';
import AnalyticsDashboard from './AnalyticsDashboard.jsx';
import NotificationCenter from './NotificationCenter.jsx';
import Gamification from './Gamification.jsx';
import About from './pages/About.jsx';
import LocationDetails from './pages/LocationDetails.jsx';
import authService from './services/auth';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is already authenticated on app load
    if (authService.isAuthenticated()) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'deals':
        return <DealsPipeline />;
      case 'clients':
        return <CRMFormsTable />;
      case 'tasks':
        return <TaskManager />;
      case 'reports':
        return <ReportsDashboard />;
      case 'email':
        return <EmailManager />;
      case 'analytics':
        return <AnalyticsDashboard />;
      case 'notifications':
        return <NotificationCenter />;
      case 'gamification':
        return <Gamification />;
      case 'programs':
        return <div className="p-6" id="programs"><h2 className="text-2xl font-bold mb-4">Programs</h2><p>Programs section coming soon...</p></div>;
      case 'settings':
        return <div className="p-6"><h2 className="text-2xl font-bold mb-4">Settings</h2><p>Settings panel coming soon...</p></div>;
      default:
        return <Dashboard />;
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Router>
      <Layout onLogout={handleLogout} activeTab={activeTab} setActiveTab={setActiveTab}>
        <Notifications />
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/deals" element={<DealsPipeline />} />
          <Route path="/clients" element={<CRMFormsTable />} />
          <Route path="/tasks" element={<TaskManager />} />
          <Route path="/reports" element={<ReportsDashboard />} />
          <Route path="/email" element={<EmailManager />} />
          <Route path="/analytics" element={<AnalyticsDashboard />} />
          <Route path="/notifications" element={<NotificationCenter />} />
          <Route path="/gamification" element={<Gamification />} />
          <Route path="/about" element={<About />} />
          <Route path="/location/:id" element={<LocationDetails />} />
          <Route path="/programs" element={<div className="p-6" id="programs"><h2 className="text-2xl font-bold mb-4">Programs</h2><p>Programs section coming soon...</p></div>} />
          <Route path="/settings" element={<div className="p-6"><h2 className="text-2xl font-bold mb-4">Settings</h2><p>Settings panel coming soon...</p></div>} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;

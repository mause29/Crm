import React, { useState, useEffect } from 'react';
import './ReportsDashboard.css';

const ReportsDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [reportsData, setReportsData] = useState({
    sales: null,
    tasks: null,
    clients: null,
    gamification: null,
    performance: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReportData = async (reportType) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/reports/${reportType}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch ${reportType} report`);
      }

      const data = await response.json();
      setReportsData(prev => ({
        ...prev,
        [reportType]: data
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReportData('performance');
  }, []);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (!reportsData[tab]) {
      fetchReportData(tab === 'overview' ? 'performance' : tab);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatPercentage = (value) => {
    return `${value.toFixed(1)}%`;
  };

  const renderOverviewTab = () => {
    const data = reportsData.performance;
    if (!data) return <div className="loading">Loading overview data...</div>;

    return (
      <div className="overview-grid">
        <div className="metric-card">
          <h3>Total Revenue</h3>
          <div className="metric-value">{formatCurrency(data.overall_metrics.total_revenue)}</div>
          <div className="metric-change positive">
            +{formatPercentage(data.monthly_growth.revenue_growth)} from last month
          </div>
        </div>

        <div className="metric-card">
          <h3>Total Clients</h3>
          <div className="metric-value">{data.overall_metrics.total_clients}</div>
          <div className="metric-change positive">
            +{formatPercentage(data.monthly_growth.client_growth)} from last month
          </div>
        </div>

        <div className="metric-card">
          <h3>Active Opportunities</h3>
          <div className="metric-value">{data.overall_metrics.total_opportunities}</div>
        </div>

        <div className="metric-card">
          <h3>Total Tasks</h3>
          <div className="metric-value">{data.overall_metrics.total_tasks}</div>
        </div>

        <div className="top-performers">
          <h3>Top Performers</h3>
          <div className="performers-list">
            {data.top_performers.map((performer, index) => (
              <div key={index} className="performer-item">
                <span className="performer-name">{performer.user}</span>
                <span className="performer-sales">{formatCurrency(performer.total_sales)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderSalesTab = () => {
    const data = reportsData.sales;
    if (!data) return <div className="loading">Loading sales data...</div>;

    return (
      <div className="sales-reports">
        <div className="chart-container">
          <h3>Sales Trend</h3>
          <div className="sales-chart">
            {data.sales_trend.map((item, index) => (
              <div key={index} className="chart-bar">
                <div className="bar-label">{item.period}</div>
                <div
                  className="bar"
                  style={{ height: `${(item.revenue / 10000) * 100}px` }}
                >
                  {formatCurrency(item.revenue)}
                </div>
                <div className="bar-subtext">{item.invoice_count} invoices</div>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-container">
          <h3>Conversion Trend</h3>
          <div className="conversion-chart">
            {data.conversion_trend.map((item, index) => (
              <div key={index} className="conversion-item">
                <span className="period">{item.period}</span>
                <span className="opportunities">{item.total_opportunities} opportunities</span>
                <span className="conversion-rate">{formatPercentage(item.conversion_rate)} won</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderTasksTab = () => {
    const data = reportsData.tasks;
    if (!data) return <div className="loading">Loading tasks data...</div>;

    return (
      <div className="tasks-reports">
        <div className="task-metrics">
          <div className="metric-card">
            <h3>Total Tasks</h3>
            <div className="metric-value">{data.summary.total_tasks}</div>
          </div>
          <div className="metric-card">
            <h3>Completion Rate</h3>
            <div className="metric-value">{formatPercentage(data.summary.completion_rate)}</div>
          </div>
          <div className="metric-card">
            <h3>Overdue Tasks</h3>
            <div className="metric-value">{data.summary.overdue_tasks}</div>
          </div>
        </div>

        <div className="task-breakdown">
          <div className="breakdown-section">
            <h3>Tasks by Priority</h3>
            {Object.entries(data.by_priority).map(([priority, stats]) => (
              <div key={priority} className="priority-item">
                <span className="priority-label">{priority}</span>
                <div className="priority-bar">
                  <div
                    className="completed-bar"
                    style={{ width: `${(stats.completed / stats.total) * 100}%` }}
                  ></div>
                </div>
                <span className="priority-stats">{stats.completed}/{stats.total}</span>
              </div>
            ))}
          </div>

          <div className="breakdown-section">
            <h3>Tasks by Status</h3>
            {Object.entries(data.by_status).map(([status, count]) => (
              <div key={status} className="status-item">
                <span className="status-label">{status}</span>
                <span className="status-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderClientsTab = () => {
    const data = reportsData.clients;
    if (!data) return <div className="loading">Loading clients data...</div>;

    return (
      <div className="clients-reports">
        <div className="client-acquisition">
          <h3>Client Acquisition Trend</h3>
          <div className="acquisition-chart">
            {data.acquisition_trend.map((item, index) => (
              <div key={index} className="acquisition-item">
                <span className="period">{item.period}</span>
                <span className="new-clients">{item.new_clients} new clients</span>
              </div>
            ))}
          </div>
        </div>

        <div className="top-clients">
          <h3>Top Clients by Revenue</h3>
          <div className="clients-list">
            {data.top_clients_by_revenue.map((client, index) => (
              <div key={index} className="client-item">
                <div className="client-info">
                  <span className="client-name">{client.name}</span>
                  <span className="client-email">{client.email}</span>
                </div>
                <div className="client-metrics">
                  <span className="revenue">{formatCurrency(client.total_revenue)}</span>
                  <span className="invoices">{client.invoice_count} invoices</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="client-engagement">
          <h3>Client Engagement</h3>
          <div className="engagement-list">
            {data.client_engagement.map((client, index) => (
              <div key={index} className="engagement-item">
                <span className="client-name">{client.name}</span>
                <div className="engagement-metrics">
                  <span>{client.total_opportunities} opportunities</span>
                  <span>{formatPercentage(client.conversion_rate)} conversion</span>
                  <span>{formatCurrency(client.avg_opportunity_value)} avg value</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderGamificationTab = () => {
    const data = reportsData.gamification;
    if (!data) return <div className="loading">Loading gamification data...</div>;

    return (
      <div className="gamification-reports">
        <div className="leaderboard">
          <h3>Points Leaderboard</h3>
          <div className="leaderboard-list">
            {data.points_leaderboard.map((user, index) => (
              <div key={index} className="leaderboard-item">
                <span className="rank">#{index + 1}</span>
                <span className="user-email">{user.user}</span>
                <span className="points">{user.total_points} points</span>
                <span className="activities">{user.activities_count} activities</span>
              </div>
            ))}
          </div>
        </div>

        <div className="achievements">
          <h3>Achievement Distribution</h3>
          <div className="achievements-list">
            {data.achievement_distribution.map((achievement, index) => (
              <div key={index} className="achievement-item">
                <div className="achievement-info">
                  <span className="achievement-name">{achievement.achievement_name}</span>
                  <span className="achievement-desc">{achievement.description}</span>
                </div>
                <span className="unlocked-count">{achievement.unlocked_count} unlocked</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="reports-dashboard">
      <div className="reports-header">
        <h1>Reports & Analytics</h1>
        <div className="reports-tabs">
          <button
            className={activeTab === 'overview' ? 'active' : ''}
            onClick={() => handleTabChange('overview')}
          >
            Overview
          </button>
          <button
            className={activeTab === 'sales' ? 'active' : ''}
            onClick={() => handleTabChange('sales')}
          >
            Sales
          </button>
          <button
            className={activeTab === 'tasks' ? 'active' : ''}
            onClick={() => handleTabChange('tasks')}
          >
            Tasks
          </button>
          <button
            className={activeTab === 'clients' ? 'active' : ''}
            onClick={() => handleTabChange('clients')}
          >
            Clients
          </button>
          <button
            className={activeTab === 'gamification' ? 'active' : ''}
            onClick={() => handleTabChange('gamification')}
          >
            Gamification
          </button>
        </div>
      </div>

      <div className="reports-content">
        {error && <div className="error-message">{error}</div>}
        {loading && <div className="loading-spinner">Loading...</div>}

        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'sales' && renderSalesTab()}
        {activeTab === 'tasks' && renderTasksTab()}
        {activeTab === 'clients' && renderClientsTab()}
        {activeTab === 'gamification' && renderGamificationTab()}
      </div>
    </div>
  );
};

export default ReportsDashboard;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
  const [overviewData, setOverviewData] = useState(null);
  const [revenueData, setRevenueData] = useState([]);
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');

      // Fetch overview data
      const overviewResponse = await axios.get('http://127.0.0.1:8000/analytics/dashboard/overview', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOverviewData(overviewResponse.data);

      // Fetch revenue chart data
      const revenueResponse = await axios.get('http://127.0.0.1:8000/analytics/revenue/chart', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRevenueData(revenueResponse.data);

      // Fetch performance metrics
      const performanceResponse = await axios.get('http://127.0.0.1:8000/analytics/performance/metrics', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPerformanceData(performanceResponse.data);

    } catch (error) {
      console.error('Error fetching analytics data:', error);
      setError('Failed to load analytics data. Please try again.');
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <div className="analytics-dashboard">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-dashboard">
        <div className="error-message">
          <h3>⚠️ Error Loading Analytics</h3>
          <p>{error}</p>
          <button onClick={fetchAnalyticsData} className="retry-btn">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h1>Analytics Dashboard</h1>
        <button onClick={fetchAnalyticsData} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {overviewData && (
        <>
          {/* Key Metrics Cards */}
          <div className="metrics-grid">
            <div className="metric-card revenue">
              <h3>Total Revenue</h3>
              <div className="metric-value">
                {formatCurrency(overviewData.revenue.total)}
              </div>
              <div className="metric-change">
                {overviewData.revenue.growth_percentage > 0 ? '+' : ''}
                {overviewData.revenue.growth_percentage.toFixed(1)}% vs last month
              </div>
            </div>

            <div className="metric-card clients">
              <h3>Total Clients</h3>
              <div className="metric-value">
                {overviewData.clients.total}
              </div>
              <div className="metric-change">
                +{overviewData.clients.new_this_month} new this month
              </div>
            </div>

            <div className="metric-card opportunities">
              <h3>Total Opportunities</h3>
              <div className="metric-value">
                {overviewData.opportunities.total}
              </div>
            </div>

            <div className="metric-card tasks">
              <h3>Task Completion</h3>
              <div className="metric-value">
                {formatPercentage(overviewData.tasks.completion_rate)}
              </div>
              <div className="metric-change">
                {overviewData.tasks.completed}/{overviewData.tasks.total} completed
              </div>
            </div>
          </div>

          {/* Revenue Chart Placeholder */}
          <div className="chart-section">
            <h2>Revenue Trend</h2>
            <div className="chart-placeholder">
              <div className="chart-data">
                {revenueData.slice(-6).map((item, index) => (
                  <div key={index} className="chart-bar">
                    <div
                      className="bar-fill"
                      style={{
                        height: `${(item.revenue / Math.max(...revenueData.map(d => d.revenue))) * 100}%`
                      }}
                    ></div>
                    <span className="bar-label">{item.period}</span>
                    <span className="bar-value">{formatCurrency(item.revenue)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Performance Insights */}
          {performanceData && (
            <div className="insights-section">
              <h2>Performance Insights</h2>
              <div className="insights-grid">
                <div className="insight-card">
                  <h4>Sales Performance</h4>
                  <p>Opportunities Created: <strong>{performanceData.sales_performance.opportunities_created}</strong></p>
                  <p>Conversion Rate: <strong>{formatPercentage(performanceData.sales_performance.conversion_rate)}</strong></p>
                  <p>Average Deal Size: <strong>{formatCurrency(performanceData.sales_performance.average_deal_size)}</strong></p>
                </div>

                <div className="insight-card">
                  <h4>Task Management</h4>
                  <p>Tasks Completed: <strong>{overviewData.tasks.completed}</strong></p>
                  <p>Overdue Tasks: <strong>{overviewData.tasks.overdue}</strong></p>
                  <p>Completion Rate: <strong>{formatPercentage(overviewData.tasks.completion_rate)}</strong></p>
                </div>

                <div className="insight-card">
                  <h4>Gamification</h4>
                  <p>Total Points: <strong>{overviewData.gamification.total_points}</strong></p>
                  <p>Keep up the great work! 🎯</p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AnalyticsDashboard;

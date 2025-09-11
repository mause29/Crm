import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [metrics, setMetrics] = useState({});
  const [salesFunnel, setSalesFunnel] = useState([]);
  const [revenueChart, setRevenueChart] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [performanceKPIs, setPerformanceKPIs] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError(null);
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [metricsRes, funnelRes, revenueRes, activityRes, kpisRes] = await Promise.all([
        axios.get('http://localhost:8000/dashboard/metrics', { headers }),
        axios.get('http://localhost:8000/dashboard/sales-funnel', { headers }),
        axios.get('http://localhost:8000/dashboard/revenue-chart', { headers }),
        axios.get('http://localhost:8000/dashboard/recent-activity', { headers }),
        axios.get('http://localhost:8000/dashboard/performance-kpis', { headers })
      ]);

      setMetrics(metricsRes.data);
      setSalesFunnel(funnelRes.data);
      setRevenueChart(revenueRes.data);
      setRecentActivity(activityRes.data);
      setPerformanceKPIs(kpisRes.data);
    } catch (err) {
      setError('Error al cargar los datos del dashboard. Verifica tu conexión.');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getMetricChange = (current, previous) => {
    if (!previous) return null;
    const change = ((current - previous) / previous) * 100;
    return {
      value: Math.abs(change),
      isPositive: change >= 0,
      formatted: `${change >= 0 ? '+' : '-'}${Math.abs(change).toFixed(1)}%`
    };
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Error al Cargar Datos</h3>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => fetchDashboardData()}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Intentar de Nuevo
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-1">Resumen general de tu rendimiento</p>
          </div>
          <button
            onClick={() => fetchDashboardData(true)}
            disabled={refreshing}
            className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 flex items-center"
          >
            {refreshing ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-500 mr-2"></div>
            ) : (
              <span className="mr-2">🔄</span>
            )}
            Actualizar
          </button>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Clientes</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.total_clients || 0}</p>
              </div>
              <div className="text-3xl">👥</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Oportunidades</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.total_opportunities || 0}</p>
              </div>
              <div className="text-3xl">🎯</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Ingresos Totales</p>
                <p className="text-2xl font-bold text-gray-900">{formatCurrency(metrics.total_revenue || 0)}</p>
              </div>
              <div className="text-3xl">💰</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Ingresos Mensuales</p>
                <p className="text-2xl font-bold text-gray-900">{formatCurrency(metrics.monthly_revenue || 0)}</p>
              </div>
              <div className="text-3xl">📈</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Oportunidades Activas</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.active_opportunities || 0}</p>
              </div>
              <div className="text-3xl">⚡</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Tus Puntos</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.user_points || 0}</p>
              </div>
              <div className="text-3xl">⭐</div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance KPIs */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Indicadores de Rendimiento</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">{performanceKPIs.conversion_rate || 0}%</div>
              <div className="text-sm font-medium text-gray-600 mb-1">Tasa de Conversión</div>
              <div className="text-xs text-gray-500">
                {performanceKPIs.won_opportunities || 0} de {performanceKPIs.total_opportunities || 0} oportunidades ganadas
              </div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">{formatCurrency(performanceKPIs.average_deal_size || 0)}</div>
              <div className="text-sm font-medium text-gray-600 mb-1">Tamaño Promedio de Acuerdos</div>
              <div className="text-xs text-gray-500">Valor promedio de acuerdos cerrados</div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">{performanceKPIs.sales_velocity_days || 0} días</div>
              <div className="text-sm font-medium text-gray-600 mb-1">Velocidad de Ventas</div>
              <div className="text-xs text-gray-500">Tiempo promedio para cerrar acuerdos</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Sales Funnel */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Embudo de Ventas</h2>
          <div className="space-y-4">
            {salesFunnel.map((stage, index) => {
              const maxCount = Math.max(...salesFunnel.map(s => s.count));
              const percentage = maxCount > 0 ? (stage.count / maxCount) * 100 : 0;

              return (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">{stage.stage}</span>
                      <span className="text-sm text-gray-500">{stage.count}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${Math.max(percentage, 5)}%` }}
                      ></div>
                    </div>
                    <div className="text-xs text-gray-500 mt-1">{formatCurrency(stage.value)}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Revenue Chart */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Tendencia de Ingresos (Últimos 12 Meses)</h2>
          <div className="flex items-end justify-between h-64 space-x-2">
            {revenueChart.map((data, index) => {
              const maxRevenue = Math.max(...revenueChart.map(d => d.revenue));
              const height = maxRevenue > 0 ? (data.revenue / maxRevenue) * 100 : 0;

              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div className="flex-1 w-full flex items-end justify-center mb-2">
                    <div
                      className="w-full bg-gradient-to-t from-blue-500 to-blue-400 rounded-t transition-all duration-300 hover:from-blue-600 hover:to-blue-500"
                      style={{ height: `${Math.max(height, 5)}%` }}
                      title={`${data.month}: ${formatCurrency(data.revenue)}`}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-500 text-center">{data.month}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="max-w-7xl mx-auto mt-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Actividad Reciente</h2>
          <div className="space-y-4">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl">
                    {activity.type === 'opportunity' ? '🎯' : activity.type === 'client' ? '👤' : '📋'}
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{activity.title}</div>
                    <div className="text-sm text-gray-600 mt-1">{activity.description}</div>
                    <div className="text-xs text-gray-500 mt-2">{formatDate(activity.date)}</div>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <div className="text-gray-400 text-4xl mb-3">📭</div>
                <p className="text-gray-500">No hay actividad reciente</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

import React, { useState } from 'react';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊', active: true },
  { id: 'deals', label: 'Deals Pipeline', icon: '💰' },
  { id: 'clients', label: 'Clients', icon: '👥' },
  { id: 'tasks', label: 'Tasks', icon: '📋' },
  { id: 'reports', label: 'Reports', icon: '📈' },
  { id: 'email', label: 'Email', icon: '📧' },
  { id: 'analytics', label: 'Analytics', icon: '📊' },
  { id: 'notifications', label: 'Notifications', icon: '🔔' },
  { id: 'gamification', label: 'Gamification', icon: '🏆' },
  { id: 'programs', label: 'Programs', icon: '📚' },
  { id: 'settings', label: 'Settings', icon: '⚙️' },
];

const Sidebar = ({ activeTab, setActiveTab }) => {
  const [expanded, setExpanded] = useState(true);

  const handleMenuClick = (itemId) => {
    setActiveTab(itemId);
  };

  return (
    <div
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
      className={`fixed top-0 left-0 h-full z-50 transition-all duration-300 ease-in-out bg-purple-700 text-white shadow-lg ${expanded ? 'w-56' : 'w-16'}`}
    >
      <div className="flex flex-col mt-4">
        {/* Logo/Brand */}
        <div className="flex items-center justify-center py-4 border-b border-purple-600">
          <div className="text-2xl font-bold">CRM</div>
        </div>

        {/* Menu Items */}
        <div className="flex flex-col space-y-2 px-2 py-4">
          {menuItems.map(item => (
            <div
              key={item.id}
              onClick={() => handleMenuClick(item.id)}
              title={item.label}
              className={`flex items-center px-4 py-3 rounded-lg cursor-pointer transition-colors duration-200 hover:bg-purple-800 ${
                activeTab === item.id ? 'bg-purple-900 border-l-4 border-white' : ''
              }`}
            >
              <div className="text-lg flex-shrink-0">{item.icon}</div>
              {expanded && (
                <span className="ml-4 font-medium text-sm whitespace-nowrap">
                  {item.label}
                </span>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        {expanded && (
          <div className="mt-auto p-4 border-t border-purple-600">
            <div className="text-xs text-purple-300">
              CRM System v1.0
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;

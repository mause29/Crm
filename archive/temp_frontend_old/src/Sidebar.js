import React from 'react';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
  { id: 'deals', label: 'Deals', icon: '💰', active: true, badge: 27 },
  { id: 'tasks', label: 'Tasks', icon: '✅', badge: 1 },
  { id: 'messages', label: 'Messages', icon: '✉️', badge: 1 },
  { id: 'calendar', label: 'Calendar', icon: '📅', badge: 1 },
  { id: 'contacts', label: 'Contacts', icon: '👥' },
  { id: 'reports', label: 'Reports', icon: '📊' },
  { id: 'products', label: 'Products', icon: '📦' },
  { id: 'store', label: 'Store', icon: '🏬' },
  { id: 'more', label: 'More', icon: '⋯' },
];

const Sidebar = () => {
  return (
    <div style={{
      width: '60px',
      backgroundColor: '#5c4ac7',
      color: 'white',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      paddingTop: '10px',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      zIndex: 1000,
    }}>
      {menuItems.map(item => (
        <div key={item.id} title={item.label} style={{
          width: '40px',
          height: '40px',
          margin: '10px 0',
          backgroundColor: item.active ? '#3b2db8' : 'transparent',
          borderRadius: '8px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          fontSize: '20px',
          userSelect: 'none',
          position: 'relative',
        }}>
          <span>{item.icon}</span>
          {item.badge && (
            <div style={{
              position: 'absolute',
              top: '-5px',
              right: '-5px',
              backgroundColor: '#ff3b30',
              color: 'white',
              borderRadius: '50%',
              width: '18px',
              height: '18px',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              boxShadow: '0 0 2px rgba(0,0,0,0.3)',
            }}>
              {item.badge}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Sidebar;

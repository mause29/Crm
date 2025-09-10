import React from 'react';

const TopBar = () => {
  return (
    <div style={{
      height: '60px',
      backgroundColor: 'white',
      borderBottom: '1px solid #ddd',
      display: 'flex',
      alignItems: 'center',
      padding: '0 20px',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      justifyContent: 'space-between',
      gap: '10px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <h2 style={{ margin: 0 }}>Deals</h2>
        <input
          type="search"
          placeholder="Search Pipedrive"
          style={{
            padding: '6px 10px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            width: '250px',
          }}
        />
        <button style={{
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          padding: '6px 12px',
          cursor: 'pointer',
          fontWeight: 'bold',
        }}>+ Deal</button>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        <button title="List View" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}>📋</button>
        <button title="Currency" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}>💲</button>
        <div style={{ fontWeight: 'bold' }}>25 350 $ · 12 deals</div>
        <button title="Pipeline View" style={{ background: 'none', border: '1px solid #ccc', borderRadius: '4px', padding: '4px 8px', cursor: 'pointer' }}>
          Pipeline ▼
        </button>
        <button title="Edit Pipeline" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}>✏️</button>
        <button title="Filter" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}>⚙️</button>
        <button title="Help" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>❓</button>
        <button title="Notifications" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>💡</button>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
          <img
            src="https://randomuser.me/api/portraits/women/44.jpg"
            alt="User"
            style={{ width: '32px', height: '32px', borderRadius: '50%' }}
          />
          <div>
            <div style={{ fontWeight: 'bold' }}>Phyllis Yang</div>
            <div style={{ fontSize: '0.8em', color: '#666' }}>Silicon Links Inc</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopBar;

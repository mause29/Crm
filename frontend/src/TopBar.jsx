import React, { useState } from 'react';

const TopBar = ({ onLogout }) => {
  const [salesMenuOpen, setSalesMenuOpen] = useState(false);
  const [analyticsMenuOpen, setAnalyticsMenuOpen] = useState(false);
  const [configMenuOpen, setConfigMenuOpen] = useState(false);
  const [moreMenuOpen, setMoreMenuOpen] = useState(false);

  return (
    <div className="h-15 bg-white border-b border-gray-300 flex items-center justify-between px-5 sticky top-0 z-50 text-sm font-medium">
      <div className="flex items-center gap-5">
        <h2 className="text-lg font-semibold">Deals</h2>
        <input
          type="search"
          placeholder="Search Pipedrive"
          className="px-3 py-1 rounded border border-gray-300 w-64"
        />
        <button className="bg-green-600 text-white rounded px-3 py-1 font-bold cursor-pointer">
          + Deal
        </button>
      </div>
      <div className="flex items-center gap-4">
        <button title="List View" className="text-xl cursor-pointer">📋</button>
        <button title="Currency" className="text-xl cursor-pointer">💲</button>
        <div className="font-bold">25 350 $ · 12 deals</div>
        <button title="Pipeline View" className="border border-gray-300 rounded px-2 py-1 cursor-pointer">
          Pipeline ▼
        </button>
        <button title="Edit Pipeline" className="text-xl cursor-pointer">✏️</button>
        <button title="Filter" className="text-xl cursor-pointer">⚙️</button>
        <button title="Help" className="text-xl cursor-pointer">❓</button>
        <button title="Notifications" className="text-xl cursor-pointer">💡</button>
        <div className="flex items-center gap-2 cursor-pointer">
          <img
            src="https://randomuser.me/api/portraits/women/44.jpg"
            alt="User"
            className="w-8 h-8 rounded-full"
          />
          <div>
            <div className="font-semibold">Phyllis Yang</div>
            <div className="text-xs text-gray-600">Silicon Links Inc</div>
          </div>
          <button
            onClick={onLogout}
            className="bg-red-600 text-white rounded px-2 py-1 text-xs ml-2 cursor-pointer"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Dropdown menus */}
      <div className="relative">
        <div
          onMouseEnter={() => setSalesMenuOpen(true)}
          onMouseLeave={() => setSalesMenuOpen(false)}
          className="inline-block cursor-pointer ml-5"
        >
          <span className="font-bold text-blue-600">Sales ▼</span>
          {salesMenuOpen && (
            <div className="absolute top-full left-0 bg-white border border-gray-300 rounded shadow p-2 z-50 min-w-[200px]">
              <div className="p-2 cursor-pointer hover:bg-gray-100">Sales channels</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Sales management</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Invoices</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Quotes</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Voice & AI scripts</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Import from 3rd party CRM</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">CRM solution presets</div>
            </div>
          )}
        </div>
        <div
          onMouseEnter={() => setAnalyticsMenuOpen(true)}
          onMouseLeave={() => setAnalyticsMenuOpen(false)}
          className="inline-block cursor-pointer ml-5"
        >
          <span className="font-bold text-blue-600">Analytics ▼</span>
          {analyticsMenuOpen && (
            <div className="absolute top-full left-0 bg-white border border-gray-300 rounded shadow p-2 z-50 min-w-[150px]">
              <div className="p-2 cursor-pointer hover:bg-gray-100">Reports</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Dashboards</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Data export</div>
            </div>
          )}
        </div>
        <div
          onMouseEnter={() => setConfigMenuOpen(true)}
          onMouseLeave={() => setConfigMenuOpen(false)}
          className="inline-block cursor-pointer ml-5"
        >
          <span className="font-bold text-blue-600">Configurations ▼</span>
          {configMenuOpen && (
            <div className="absolute top-full left-0 bg-white border border-gray-300 rounded shadow p-2 z-50 min-w-[150px]">
              <div className="p-2 cursor-pointer hover:bg-gray-100">Settings</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Users</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Permissions</div>
            </div>
          )}
        </div>
        <div
          onMouseEnter={() => setMoreMenuOpen(true)}
          onMouseLeave={() => setMoreMenuOpen(false)}
          className="inline-block cursor-pointer ml-5"
        >
          <span className="font-bold text-blue-600">More ▼</span>
          {moreMenuOpen && (
            <div className="absolute top-full left-0 bg-white border border-gray-300 rounded shadow p-2 z-50 min-w-[150px]">
              <div className="p-2 cursor-pointer hover:bg-gray-100">Help</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">About</div>
              <div className="p-2 cursor-pointer hover:bg-gray-100">Contact</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TopBar;

import React, { useState } from 'react';
import AdminEvents from './AdminEvents';
import AdminUsers from './AdminUsers';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('events');

  return (
    <div className="admin-dashboard-wrapper">
      <div className="admin-tabs">
        <div className="container">
          <div className="tabs-header">
            <button
              className={`tab-btn ${activeTab === 'events' ? 'active' : ''}`}
              onClick={() => setActiveTab('events')}
            >
              <span className="tab-icon">📊</span>
              Events
            </button>
            <button
              className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
              onClick={() => setActiveTab('users')}
            >
              <span className="tab-icon">👥</span>
              Users
            </button>
            <button
              className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
              onClick={() => setActiveTab('analytics')}
            >
              <span className="tab-icon">📈</span>
              Analytics
            </button>
          </div>
        </div>
      </div>

      <div className="admin-content">
        {activeTab === 'events' && <AdminEvents />}
        {activeTab === 'users' && <AdminUsers />}
        {activeTab === 'analytics' && (
          <div className="container" style={{ paddingTop: '60px' }}>
            <div className="empty-state">
              <span className="empty-icon">📈</span>
              <h2>Analytics Coming Soon</h2>
              <p>Detailed event statistics and reports will be available here</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;

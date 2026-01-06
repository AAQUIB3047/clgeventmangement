import React from 'react';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <h1>Welcome, {user?.first_name || user?.email}! 👋</h1>
          <p>Here's your event management dashboard</p>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card card">
            <div className="card-icon">🎫</div>
            <h3>My Bookings</h3>
            <p className="card-description">View and manage your event tickets</p>
            <a href="/my-bookings" className="btn btn-primary btn-sm">
              View Bookings
            </a>
          </div>

          <div className="dashboard-card card">
            <div className="card-icon">🔍</div>
            <h3>Explore Events</h3>
            <p className="card-description">Discover upcoming events and concerts</p>
            <a href="/" className="btn btn-primary btn-sm">
              Browse Events
            </a>
          </div>

          <div className="dashboard-card card">
            <div className="card-icon">👤</div>
            <h3>Profile</h3>
            <p className="card-description">Manage your account settings</p>
            <a href="#" className="btn btn-secondary btn-sm">
              Coming Soon
            </a>
          </div>

          {user?.role === 'admin' && (
            <div className="dashboard-card card">
              <div className="card-icon">⚙️</div>
              <h3>Admin Panel</h3>
              <p className="card-description">Manage events and users</p>
              <a href="/admin" className="btn btn-primary btn-sm">
                Go to Admin
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

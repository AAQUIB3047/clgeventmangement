import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isAuthenticated, user, onLogout }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="container flex-between">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🎫</span>
          <span className="brand-text">EventHub</span>
        </Link>

        <button 
          className={`mobile-toggle ${mobileMenuOpen ? 'active' : ''}`}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div className={`navbar-menu ${mobileMenuOpen ? 'active' : ''}`}>
          <Link to="/" className="nav-link" onClick={() => setMobileMenuOpen(false)}>
            Explore
          </Link>

          {isAuthenticated ? (
            <>
              <Link to="/my-bookings" className="nav-link" onClick={() => setMobileMenuOpen(false)}>
                My Bookings
              </Link>
              {user?.role === 'admin' && (
                <Link to="/admin" className="nav-link" onClick={() => setMobileMenuOpen(false)}>
                  Admin
                </Link>
              )}
              <div className="nav-user">
                <span className="user-name">{user?.name || user?.email}</span>
                <button 
                  className="btn btn-secondary btn-sm"
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary btn-sm" onClick={() => setMobileMenuOpen(false)}>
                Sign In
              </Link>
              <Link to="/register" className="btn btn-primary btn-sm" onClick={() => setMobileMenuOpen(false)}>
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

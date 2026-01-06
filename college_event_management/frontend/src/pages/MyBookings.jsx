import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MyBookings.css';

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        'http://localhost:8000/api/registrations/my-registrations/',
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setBookings(response.data);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="my-bookings">
      <div className="container">
        <div className="page-header">
          <h1>My Bookings 🎫</h1>
          <p>View and manage all your event tickets</p>
        </div>

        {loading ? (
          <div className="loading-grid">
            {[1, 2, 3].map(i => (
              <div key={i} className="booking-card skeleton"></div>
            ))}
          </div>
        ) : bookings.length > 0 ? (
          <div className="bookings-grid">
            {bookings.map(booking => (
              <div key={booking.id} className="booking-card card">
                <div className="booking-header">
                  <h3>{booking.event?.title || 'Event'}</h3>
                  <span className="booking-status">✓ Confirmed</span>
                </div>
                <div className="booking-details">
                  <div className="detail">
                    <span className="detail-label">📅 Date</span>
                    <span className="detail-value">
                      {new Date(booking.event?.date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="detail">
                    <span className="detail-label">🎟️ Tickets</span>
                    <span className="detail-value">{booking.quantity} Tickets</span>
                  </div>
                  <div className="detail">
                    <span className="detail-label">💰 Total</span>
                    <span className="detail-value">
                      ₹{(booking.event?.price || 0) * booking.quantity}
                    </span>
                  </div>
                </div>
                <button className="btn btn-secondary btn-sm" style={{ width: '100%' }}>
                  View Details
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">🎫</span>
            <h2>No bookings yet</h2>
            <p>Start exploring events and book your first ticket!</p>
            <a href="/" className="btn btn-primary">
              Explore Events
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default MyBookings;

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './EventDetail.css';

const EventDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [booking, setBooking] = useState(false);

  useEffect(() => {
    fetchEvent();
  }, [id]);

  const fetchEvent = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/events/${id}/`);
      setEvent(response.data);
    } catch (err) {
      setError('Failed to load event details');
    } finally {
      setLoading(false);
    }
  };

  const handleBooking = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    setBooking(true);
    try {
      await axios.post(
        `http://localhost:8000/api/registrations/`,
        { event: id, quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Booking successful!');
      navigate('/my-bookings');
    } catch (err) {
      setError(err.response?.data?.detail || 'Booking failed');
    } finally {
      setBooking(false);
    }
  };

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;

  if (!event) {
    return (
      <div className="container" style={{ paddingTop: '100px' }}>
        <div className="empty-state">
          <h2>Event not found</h2>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Back to Events
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="event-detail">
      <div className="event-hero">
        <img
          src={event.image_url || 'https://via.placeholder.com/1200x400?text=Event'}
          alt={event.title}
          className="hero-image"
        />
        <button className="back-btn" onClick={() => navigate('/')}>
          ← Back
        </button>
      </div>

      <div className="container event-content">
        <div className="event-main">
          <div className="event-info">
            <h1>{event.title}</h1>
            <div className="event-details-grid">
              <div className="detail-item">
                <span className="detail-icon">📅</span>
                <div>
                  <p className="detail-label">Date</p>
                  <p className="detail-value">
                    {new Date(event.date).toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </p>
                </div>
              </div>

              <div className="detail-item">
                <span className="detail-icon">⏰</span>
                <div>
                  <p className="detail-label">Time</p>
                  <p className="detail-value">{event.time || 'TBD'}</p>
                </div>
              </div>

              <div className="detail-item">
                <span className="detail-icon">📍</span>
                <div>
                  <p className="detail-label">Venue</p>
                  <p className="detail-value">{event.location || 'TBD'}</p>
                </div>
              </div>

              <div className="detail-item">
                <span className="detail-icon">👥</span>
                <div>
                  <p className="detail-label">Seats Available</p>
                  <p className="detail-value">{event.available_seats || 0}</p>
                </div>
              </div>
            </div>

            <div className="description-section">
              <h2>About This Event</h2>
              <p>{event.description}</p>
            </div>
          </div>

          <div className="event-booking">
            <div className="booking-card card">
              <div className="price-section">
                <span className="price-label">Price per ticket</span>
                <span className="price-value">₹{event.price || 'Free'}</span>
              </div>

              {error && <div className="alert alert-error">{error}</div>}

              <div className="quantity-section">
                <label>Number of Tickets</label>
                <div className="quantity-control">
                  <button
                    className="qty-btn"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  >
                    −
                  </button>
                  <span className="qty-value">{quantity}</span>
                  <button
                    className="qty-btn"
                    onClick={() =>
                      setQuantity(Math.min(event.available_seats || 10, quantity + 1))
                    }
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="total-section">
                <span className="total-label">Total</span>
                <span className="total-value">
                  ₹{(event.price || 0) * quantity}
                </span>
              </div>

              <button
                className="btn btn-primary btn-lg"
                onClick={handleBooking}
                disabled={booking || event.available_seats === 0}
                style={{ width: '100%' }}
              >
                {booking ? 'Booking...' : event.available_seats === 0 ? 'Sold Out' : 'Book Tickets'}
              </button>

              {event.available_seats === 0 && (
                <p className="sold-out-message">Sorry, all tickets are sold out!</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetail;

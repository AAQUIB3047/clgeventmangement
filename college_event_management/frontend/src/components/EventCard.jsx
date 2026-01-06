import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/eventcard.css';

/**
 * EventCard Component
 * Displays a single event in card format
 *
 * @param {Object} event - Event data
 * @param {string} event.id - Event ID
 * @param {string} event.title - Event title
 * @param {string} event.description - Event description
 * @param {string} event.date - Event date
 * @param {string} event.location - Event location
 * @param {number} event.capacity - Event capacity
 * @param {number} event.registered - Number registered
 * @param {string} event.image - Event image URL
 */
const EventCard = ({ event }) => {
  const registrationPercentage = (event.registered / event.capacity) * 100;
  const isFull = event.registered >= event.capacity;

  return (
    <div className="event-card">
      <div className="event-card-image">
        {event.image && <img src={event.image} alt={event.title} />}
        <div className={`event-badge ${event.status}`}>
          {event.status === 'upcoming'
            ? '📅 Upcoming'
            : event.status === 'ongoing'
              ? '🔴 Ongoing'
              : '✅ Completed'}
        </div>
      </div>

      <div className="event-card-content">
        <h3 className="event-title">{event.title}</h3>

        <div className="event-meta">
          <span className="meta-item">📅 {new Date(event.date).toLocaleDateString()}</span>
          <span className="meta-item">📍 {event.location}</span>
        </div>

        <p className="event-description">{event.description.substring(0, 100)}...</p>

        <div className="event-capacity">
          <div className="capacity-info">
            <span>
              {event.registered}/{event.capacity} Registered
            </span>
          </div>
          <div className="capacity-bar">
            <div
              className="capacity-fill"
              style={{ width: `${Math.min(registrationPercentage, 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="event-card-footer">
          <Link to={`/events/${event.id}`} className="btn-view-details">
            View Details →
          </Link>
          <button className={`btn-register ${isFull ? 'disabled' : ''}`} disabled={isFull}>
            {isFull ? 'Event Full' : 'Register'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EventCard;

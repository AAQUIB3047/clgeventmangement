import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminEvents.css';

const AdminEvents = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: '',
    time: '',
    location: '',
    price: '',
    category: 'concert',
    available_seats: '',
    image_url: '',
  });

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/events/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      // Handle both array and paginated responses
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setEvents(data);
    } catch (error) {
      setErrorMessage('Failed to fetch events');
      console.error(error);
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const payload = {
        ...formData,
        price: parseFloat(formData.price) || 0,
        available_seats: parseInt(formData.available_seats) || 0,
      };

      if (editingId) {
        // Update event
        await axios.put(
          `http://localhost:8000/api/events/${editingId}/`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setSuccessMessage('Event updated successfully!');
      } else {
        // Create event
        await axios.post(
          'http://localhost:8000/api/events/',
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setSuccessMessage('Event created successfully!');
      }

      resetForm();
      fetchEvents();
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail ||
        error.response?.data?.title?.[0] ||
        'Failed to save event'
      );
    }
  };

  const handleEdit = (event) => {
    setFormData({
      title: event.title,
      description: event.description,
      date: event.date,
      time: event.time || '',
      location: event.location || '',
      price: event.price || '',
      category: event.category || 'concert',
      available_seats: event.available_seats || '',
      image_url: event.image_url || '',
    });
    setEditingId(event.id);
    setShowForm(true);
  };

  const handleDelete = async () => {
    try {
      await axios.delete(
        `http://localhost:8000/api/events/${deleteConfirm}/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccessMessage('Event deleted successfully!');
      setDeleteConfirm(null);
      fetchEvents();
    } catch (error) {
      setErrorMessage('Failed to delete event');
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      date: '',
      time: '',
      location: '',
      price: '',
      category: 'concert',
      available_seats: '',
      image_url: '',
    });
    setEditingId(null);
    setShowForm(false);
  };

  const filteredEvents = Array.isArray(events) ? events.filter(event =>
    event.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.description?.toLowerCase().includes(searchQuery.toLowerCase())
  ) : [];

  return (
    <div className="admin-events">
      <div className="container">
        <div className="admin-header">
          <div className="header-content">
            <h1>📊 Event Management</h1>
            <p>Create, edit, and delete events</p>
          </div>
          <button
            className="btn btn-primary btn-lg"
            onClick={() => !showForm ? setShowForm(true) : resetForm()}
          >
            {showForm ? '✕ Cancel' : '+ Create Event'}
          </button>
        </div>

        {successMessage && (
          <div className="alert alert-success">
            ✓ {successMessage}
          </div>
        )}

        {errorMessage && (
          <div className="alert alert-error">
            ✕ {errorMessage}
          </div>
        )}

        {showForm && (
          <div className="form-section card">
            <h2>{editingId ? 'Edit Event' : 'Create New Event'}</h2>
            <form onSubmit={handleSubmit} className="event-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="title">Event Title *</label>
                  <input
                    id="title"
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    placeholder="E.g., Summer Concert 2025"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="category">Category *</label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="concert">Concert</option>
                    <option value="conference">Conference</option>
                    <option value="sports">Sports</option>
                    <option value="workshop">Workshop</option>
                    <option value="festival">Festival</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="description">Description *</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Describe the event in detail..."
                  rows="4"
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="date">Date *</label>
                  <input
                    id="date"
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="time">Time</label>
                  <input
                    id="time"
                    type="time"
                    name="time"
                    value={formData.time}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="location">Location *</label>
                  <input
                    id="location"
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    placeholder="E.g., Main Auditorium"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="price">Price (₹)</label>
                  <input
                    id="price"
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleInputChange}
                    placeholder="0"
                    min="0"
                    step="10"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="available_seats">Available Seats *</label>
                  <input
                    id="available_seats"
                    type="number"
                    name="available_seats"
                    value={formData.available_seats}
                    onChange={handleInputChange}
                    placeholder="100"
                    min="1"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="image_url">Image URL</label>
                  <input
                    id="image_url"
                    type="url"
                    name="image_url"
                    value={formData.image_url}
                    onChange={handleInputChange}
                    placeholder="https://example.com/image.jpg"
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary btn-lg">
                  {editingId ? '✓ Update Event' : '+ Create Event'}
                </button>
                <button
                  type="button"
                  className="btn btn-secondary btn-lg"
                  onClick={resetForm}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="search-section">
          <input
            type="text"
            placeholder="🔍 Search events by name or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <span className="result-count">{filteredEvents.length} events</span>
        </div>

        {loading ? (
          <div className="loading-grid">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="event-row skeleton"></div>
            ))}
          </div>
        ) : filteredEvents.length > 0 ? (
          <div className="events-table">
            <div className="table-header">
              <div className="col-title">Event</div>
              <div className="col-date">Date</div>
              <div className="col-location">Location</div>
              <div className="col-price">Price</div>
              <div className="col-seats">Seats</div>
              <div className="col-actions">Actions</div>
            </div>

            {filteredEvents.map(event => (
              <div key={event.id} className="table-row">
                <div className="col-title">
                  <div className="event-name">{event.title}</div>
                  <div className="event-category">{event.category}</div>
                </div>

                <div className="col-date">
                  {new Date(event.date).toLocaleDateString()}
                </div>

                <div className="col-location">{event.location}</div>

                <div className="col-price">
                  ₹{event.price || 'Free'}
                </div>

                <div className="col-seats">
                  <span className={`seats-badge ${event.available_seats > 0 ? 'available' : 'sold-out'}`}>
                    {event.available_seats} seats
                  </span>
                </div>

                <div className="col-actions">
                  <button
                    className="btn btn-sm btn-primary"
                    onClick={() => handleEdit(event)}
                    title="Edit event"
                  >
                    ✎ Edit
                  </button>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => setDeleteConfirm(event.id)}
                    title="Delete event"
                  >
                    🗑 Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📭</span>
            <h3>No events found</h3>
            <p>
              {searchQuery
                ? 'Try adjusting your search'
                : 'Create your first event to get started'}
            </p>
          </div>
        )}
      </div>

      {deleteConfirm && (
        <div className="modal-overlay" onClick={() => setDeleteConfirm(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>Delete Event?</h2>
            <p>
              Are you sure you want to delete this event? This action cannot be undone.
            </p>
            <div className="modal-actions">
              <button
                className="btn btn-danger btn-lg"
                onClick={handleDelete}
              >
                🗑 Delete
              </button>
              <button
                className="btn btn-secondary btn-lg"
                onClick={() => setDeleteConfirm(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminEvents;

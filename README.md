# College Event Management System

A modern, full-stack web application for managing college events with role-based access control. Built with Django REST Framework backend and React frontend.

## Features

- **User Authentication**: Secure login with JWT tokens
- **Role-Based Access**: Student, Organizer, and Admin roles
- **Event Management**: Create, update, and manage college events
- **Registration System**: Students can register for events
- **Attendance Tracking**: Mark and track event attendance
- **Admin Dashboard**: Comprehensive admin controls
- **Responsive Design**: Mobile-friendly interface
- **Modern UI**: Green and white theme inspired by BookMyShow

## Tech Stack

### Backend
- **Django 5.1.1** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database
- **JWT Authentication** - Token-based auth
- **CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI library
- **Axios** - HTTP client
- **React Router** - Navigation
- **CSS3** - Styling with modern design

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd college_event_management/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Add sample data (optional):**
   ```bash
   python ../../add_events.py
   python ../../add_user.py
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd college_event_management/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```

## Usage

### Default Users

- **Admin User:**
  - Username: `admin`
  - Email: `admin@example.com`
  - Password: Set during setup

- **Test User:**
  - Username: `aaquib`
  - Email: `qureshiaaquib1304@gmail.com`
  - Password: `aaquib1304`

### API Endpoints

- `POST /api/auth/login/` - User login
- `GET /api/events/` - List events
- `POST /api/events/` - Create event (Admin/Organizer)
- `GET /api/dashboard/` - User dashboard
- `GET /api/admin/dashboard/` - Admin dashboard

## Project Structure

```
college_event_management/
├── backend/                 # Django backend
│   ├── event_management/    # Main Django project
│   ├── users/              # User management app
│   ├── events/             # Event management app
│   ├── registrations/      # Registration app
│   ├── attendance/         # Attendance tracking app
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.js         # Main app component
│   └── package.json       # Node dependencies
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Backend
cd backend
python manage.py collectstatic

# Frontend
cd frontend
npm run build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.

# 🎫 EventHub - Modern College Event Management System

A sleek, modern **BookMyShow-inspired** event management platform with a **Gen Z aesthetic** featuring **green, white, and black** theme.

## ✨ Features

### User-Facing Features
- **🎯 Modern Home Page**: Hero section with category filters and event discovery
- **🔐 Authentication**: Secure login/register with JWT tokens
- **📱 Responsive Design**: Works flawlessly on desktop, tablet, and mobile
- **🎫 Event Browsing**: Browse, filter, and search events
- **💳 Ticket Booking**: Easy one-click booking with quantity controls
- **👤 My Bookings**: View all your purchased tickets
- **📊 User Dashboard**: Quick access to bookings and profile

### Admin Features
- **⚙️ Admin Panel**: Dashboard for event management
- **👥 User Management**: Control user accounts and roles
- **📈 Analytics**: View event statistics and registration data

## 🎨 Design System

### Color Palette
- **Primary Green**: `#22c55e` - Vibrant, modern, eye-catching
- **Dark Green**: `#16a34a` - Depth and contrast
- **Light Green**: `#dcfce7` - Subtle accents
- **Dark Background**: `#0f172a` - Premium dark mode
- **Card Background**: `#1e293b` - Sleek surfaces
- **White**: `#ffffff` - Text and highlights
- **Black**: `#000000` - Maximum contrast

### Typography
- **Font Family**: Poppins, Inter, system fonts
- **Font Weights**: 400 (regular), 600 (semibold), 700 (bold), 800 (extra bold)
- **Responsive**: Scales beautifully from mobile to desktop

### Components
- **Buttons**: Gradient backgrounds, hover animations, multiple sizes
- **Cards**: Glassmorphism effect with subtle borders
- **Forms**: Smooth focus states with green accents
- **Navigation**: Sticky navbar with mobile hamburger menu
- **Loading**: Animated spinner with green theme

## 🗂️ Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.js & Home.css           # Landing page with event grid
│   │   ├── Login.js                     # User login page
│   │   ├── Register.js                  # User registration page
│   │   ├── EventDetail.js & .css        # Event detail and booking
│   │   ├── Dashboard.js & .css          # User dashboard
│   │   ├── MyBookings.js & .css         # User bookings list
│   │   ├── AdminDashboard.js & .css     # Admin control panel
│   │   └── Auth.css                     # Auth pages styling
│   ├── components/
│   │   ├── Navbar.js & Navbar.css       # Navigation bar
│   │   └── ...
│   ├── styles/
│   │   └── theme.css                    # Global theme variables and utilities
│   ├── App.js & App.css                 # Main app component with routing
│   ├── index.js                         # React entry point
│   ├── index.css                        # Global styles
│   └── ...
├── package.json                         # Dependencies and scripts
└── ...
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend running on `http://localhost:8000`

### Installation

```bash
cd college_event_management/frontend
npm install
```

### Development

```bash
npm start
```

Opens [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
```

Creates optimized production build in the `build` folder.

## 🔗 API Integration

The frontend communicates with the Django backend via REST API:

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

### Event Endpoints
- `GET /api/events/` - Get all events
- `GET /api/events/{id}/` - Get single event details

### Booking Endpoints
- `POST /api/registrations/` - Create booking
- `GET /api/registrations/my-registrations/` - Get user bookings

## 🛠️ Technologies Used

- **React 18** - UI library
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients, animations, and flexbox
- **react-scripts 5.0.1** - Build tooling

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: Below 768px

All pages are fully responsive and optimized for all screen sizes.

## 🎯 Key Features Breakdown

### Home Page
- Animated hero section with gradient text
- Category filter buttons
- Event search functionality
- Grid layout with hover animations
- Skeleton loading states

### Authentication
- Email/password login
- User registration with validation
- Password confirmation
- JWT token storage
- Secure logout

### Event Details
- Full event information display
- High-quality event images
- Quantity selector for tickets
- Real-time price calculation
- Booking confirmation

### Dashboard
- Quick access links
- User greeting
- Role-based content (admin panel for admins)
- Card-based layout

### My Bookings
- List of all user bookings
- Booking status display
- Event details per booking
- Empty state for new users

## 🎬 Animations & Interactions

- **Smooth Scrolling**: HTML scroll-behavior
- **Fade In**: Elements fade in on load
- **Slide Transitions**: Cards and components slide in
- **Hover Effects**: Cards lift and change colors on hover
- **Floating Emojis**: Subtle animation in hero section
- **Loading Spinners**: Animated green spinners

## ⚡ Performance

- **Production Build Size**: ~76.94 kB (gzipped)
- **Optimized Images**: Lazy loading ready
- **CSS Bundling**: Automatic critical CSS extraction
- **Code Splitting**: React Router lazy loading compatible

## 🔒 Security

- **JWT Authentication**: Secure token-based auth
- **Secure Storage**: Tokens stored in localStorage
- **CORS**: Configured for frontend-backend communication
- **Protected Routes**: Authenticated routes guard access

## 📝 Environment Variables

Create a `.env` file in the frontend directory (optional):

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

## 🚨 Troubleshooting

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -r node_modules package-lock.json
npm install
npm start
```

### Backend connection issues
- Ensure Django backend is running on `http://localhost:8000`
- Check CORS settings in Django `settings.py`
- Verify API endpoints in browser DevTools

### Build errors
```bash
npm run build 2>&1 | grep -i error
```

## 📚 Available Scripts

- `npm start` - Start development server
- `npm build` - Create production build
- `npm test` - Run test suite
- `npm eject` - Eject from create-react-app (irreversible)

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [React Router](https://reactrouter.com)
- [Axios](https://axios-http.com)
- [Modern CSS](https://web.dev/learn/css)

## 👥 Contributors

Built with ❤️ for the college event management system.

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated**: December 29, 2025  
**Frontend Version**: 1.0.0  
**React Version**: 18.2.0

🚀 **Ready to deploy and fully functional!**

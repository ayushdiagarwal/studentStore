# Student Store Frontend

A React-based frontend application for the Student Store with Google OAuth authentication.

## Features

- **Google OAuth Authentication**: Secure sign-in using Google accounts
- **User Management**: Automatic user creation and profile management
- **Protected Routes**: Secure access to authenticated features
- **Responsive Design**: Modern UI built with Tailwind CSS
- **TypeScript**: Full type safety and better development experience

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running (see backend setup)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Build CSS:
```bash
npm run build:css
```

3. Start development server:
```bash
npm run dev
```

## Environment Configuration

Create a `.env` file in the frontend directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8002/api/v1

# Google OAuth Configuration (if needed for frontend)
VITE_GOOGLE_CLIENT_ID=your_google_client_id

# App Configuration
VITE_APP_NAME=Student Store
VITE_APP_VERSION=1.0.0
```

## Google OAuth Setup

### 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Configure the OAuth consent screen
6. Set application type to "Web application"
7. Add authorized redirect URIs:
   - `http://localhost:8002/api/v1/auth/google/callback` (for backend)
   - `http://localhost:5173/auth/google/callback` (for frontend development)

### 2. Backend Configuration

Update your backend `.env` file with the Google OAuth credentials:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8002/api/v1/auth/google/callback
JWT_SECRET_KEY=your-super-secret-jwt-key
```

### 3. Frontend Configuration

The frontend will automatically use the backend API for authentication. No additional Google OAuth configuration is needed in the frontend.

## Authentication Flow

1. **User clicks "Sign in with Google"**
   - Frontend requests Google OAuth URL from backend
   - User is redirected to Google's consent screen

2. **Google OAuth Callback**
   - Google redirects back to backend with authorization code
   - Backend exchanges code for access token
   - Backend creates/updates user and returns JWT token

3. **Frontend receives token**
   - Token is stored in localStorage
   - User is redirected to home page
   - Protected features become available

4. **Authenticated requests**
   - Frontend automatically includes JWT token in API requests
   - Backend validates token and returns user data

## Project Structure

```
src/
├── components/          # React components
│   ├── LoginButton.tsx     # Google OAuth login button
│   ├── UserProfile.tsx     # User profile and logout
│   ├── GoogleCallback.tsx  # OAuth callback handler
│   ├── ProtectedRoute.tsx  # Route protection component
│   └── ...
├── contexts/           # React contexts
│   └── AuthContext.tsx     # Authentication state management
├── services/           # API services
│   └── auth.ts             # Authentication API calls
├── types/              # TypeScript type definitions
│   └── auth.ts             # Authentication types
└── ...
```

## Key Components

### AuthContext
Manages global authentication state including:
- User information
- Authentication status
- Login/logout functions
- Token management

### LoginButton
- Triggers Google OAuth flow
- Shows loading state during authentication
- Styled with Google branding

### UserProfile
- Displays user information
- Shows profile picture (if available)
- Provides logout functionality

### GoogleCallback
- Handles OAuth callback from Google
- Processes authorization code
- Manages authentication completion

### ProtectedRoute
- Wraps routes that require authentication
- Redirects unauthenticated users
- Shows loading state during auth check

## API Integration

The frontend communicates with the backend through the `authService`:

- **GET** `/auth/google/login` - Get Google OAuth URL
- **POST** `/auth/google/callback` - Handle OAuth callback
- **GET** `/auth/me` - Get current user information
- **POST** `/auth/logout` - Logout user

## Security Features

- JWT token-based authentication
- Automatic token refresh
- Secure token storage in localStorage
- Automatic logout on token expiration
- Protected route components

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build:css` - Build Tailwind CSS
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Protected Routes

```tsx
import ProtectedRoute from './components/ProtectedRoute';

<Route 
  path="/protected" 
  element={
    <ProtectedRoute>
      <ProtectedComponent />
    </ProtectedRoute>
  } 
/>
```

### Customizing Authentication

The authentication system is designed to be extensible:

- Add new OAuth providers in `authService`
- Extend user model in `types/auth.ts`
- Add new protected routes using `ProtectedRoute`
- Customize authentication UI components

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS is configured for frontend origin
2. **Authentication Failed**: Check Google OAuth credentials and redirect URIs
3. **Token Expired**: Frontend automatically handles token expiration
4. **User Not Found**: Verify backend user creation logic

### Debug Mode

Enable debug logging in the browser console to see authentication flow details.

## Production Deployment

1. Update environment variables for production
2. Configure proper CORS origins
3. Use HTTPS for OAuth redirect URIs
4. Set secure JWT secret keys
5. Configure proper domain names

## Contributing

1. Follow TypeScript best practices
2. Use functional components with hooks
3. Maintain consistent styling with Tailwind CSS
4. Add proper error handling
5. Test authentication flows thoroughly

# JWT OAuth API - Production-Grade REST API

A modern, production-ready REST API built with FastAPI, featuring JWT authentication, OAuth2 integration (Google & GitHub), RBAC, rate limiting, and comprehensive testing.

## Features

- **JWT Authentication**: Secure token-based authentication with access and refresh tokens
- **OAuth2 Integration**:  Sign in with Google or GitHub
- **Role-Based Access Control (RBAC)**: Admin and user roles
- **Rate Limiting**: Prevent abuse with configurable rate limits
- **Task Management**: Full CRUD operations for tasks with ownership
- **Database Migrations**: Alembic for schema versioning
- **Comprehensive Testing**: 20+ unit and integration tests
- **Docker Support**: Ready for containerized deployment
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Project Structure

```
jwt-oauth-api/
├── app/
│   ├── models/           # Database models (User, Task, OAuthAccount)
│   ├── routers/          # API endpoints
│   ├── schemas/          # Pydantic schemas for validation
│   ├── services/         # Business logic
│   ├── utils/            # Utilities (JWT, password hashing, rate limiter)
│   ├── database.py       # Database configuration
│   ├── config.py         # App configuration
│   ├── dependencies.py   # Dependency injection
│   ├── exceptions.py     # Custom exceptions
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
├── tests/                # Test suite
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── docker-compose.yml    # Docker services
```

## Installation

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jwt-oauth-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Setup database**
   ```bash
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

Visit `http://localhost:8000/docs` for API documentation.

## API Endpoints

### Authentication

#### Sign Up
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### OAuth

#### Google OAuth Callback
```http
POST /oauth/google/callback?code=AUTH_CODE
```

#### GitHub OAuth Callback
```http
POST /oauth/github/callback?code=AUTH_CODE
```

### Users

#### Get Current User Profile
```http
GET /users/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z",
  "oauth_accounts": []
}
```

#### Update Profile
```http
PUT /users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "password": "newpassword"
}
```

#### Get User (Admin Only)
```http
GET /users/{user_id}
Authorization: Bearer <admin_token>
```

#### List All Users (Admin Only)
```http
GET /users
Authorization: Bearer <admin_token>
```

### Tasks

#### Create Task
```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the JWT OAuth API"
}
```

**Response:**
```json
{
  "id": "650e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project",
  "description": "Finish the JWT OAuth API",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

#### List User's Tasks
```http
GET /tasks
Authorization: Bearer <access_token>
```

#### Get Task
```http
GET /tasks/{task_id}
Authorization: Bearer <access_token>
```

#### Update Task
```http
PUT /tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}
```

#### Delete Task
```http
DELETE /tasks/{task_id}
Authorization: Bearer <access_token>
```

## Database

### Models

**User**
- `id` (UUID): Primary key
- `email` (String): Unique email address
- `hashed_password` (String): BCrypt hashed password (nullable for OAuth users)
- `is_active` (Boolean): Account status
- `is_admin` (Boolean): Admin privilege flag
- `created_at` (DateTime): Creation timestamp
- Relations: `oauth_accounts`, `tasks`

**OAuthAccount**
- `id` (UUID): Primary key
- `user_id` (UUID): Foreign key to User
- `provider` (String): OAuth provider ('google' or 'github')
- `account_id` (String): Provider's user ID
- `account_email` (String): Email from provider

**Task**
- `id` (UUID): Primary key
- `title` (String): Task title
- `description` (Text): Task description
- `owner_id` (UUID): Foreign key to User
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Check current migration:
```bash
alembic current
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_auth.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

- **Authentication**: Signup, login, token refresh, invalid credentials
- **OAuth**: Google and GitHub OAuth flows
- **Users**: Profile management, admin operations
- **Tasks**: CRUD operations, permissions, ownership

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/jwt_api

# JWT
SECRET_KEY=your-super-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth - Google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OAuth - GitHub
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# App
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

## Security Best Practices

1. **JWT Secret**: Use a strong, random secret key (minimum 32 characters)
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Configured to prevent brute force attacks
4. **Password Hashing**: BCrypt with configurable rounds
5. **CORS**: Configure carefully for production
6. **API Keys**: Store sensitive keys in environment variables
7. **Token Expiration**: Access tokens expire in 15 minutes by default

## Rate Limiting

Endpoints have rate limits:
- `/auth/signup`: 5 requests per minute
- `/auth/login`: 10 requests per minute
- `/tasks`: 20 requests per minute

## Docker Deployment

Build and run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Run migrations: `alembic upgrade head`

### Token Validation Errors
- Verify SECRET_KEY matches between token generation and validation
- Check token expiration times
- Ensure proper Authorization header format: `Authorization: Bearer <token>`

### OAuth Errors
- Verify OAuth credentials in .env
- Check callback URLs match provider settings
- Ensure frontend URL matches provider configuration

## Development

### Code Style
```bash
# Format code
black app/ tests/

# Lint
pylint app/

# Type checking
mypy app/
```

### Adding New Endpoints

1. Create schema in `app/schemas/`
2. Add business logic in `app/services/`
3. Create router in `app/routers/`
4. Include router in `app/main.py`
5. Write tests in `tests/`
6. Update migrations if model changes

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository.

## Roadmap

- [ ] WebSocket support for real-time task updates
- [ ] Email verification for signup
- [ ] Two-factor authentication (2FA)
- [ ] Team collaboration features
- [ ] Task categories and filtering
- [ ] Audit logging
- [ ] API rate limit per user tier
- [ ] GraphQL endpoint

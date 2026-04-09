# JWT OAuth API

A production-grade REST API featuring JWT authentication, OAuth2 (Google & GitHub), RBAC, rate limiting, and comprehensive task management.

## Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- (Optional) Docker & Docker Compose

### Installation

```bash
# Clone repository
git clone <repo-url> && cd jwt-oauth-api

# Create virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database and OAuth credentials

# Setup database
alembic upgrade head

# Run server
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

## Key Features

✅ **JWT Authentication** - Access & refresh tokens with configurable expiration  
✅ **OAuth2 Integration** - Sign in with Google or GitHub  
✅ **Role-Based Access Control** - Admin and regular user roles  
✅ **Rate Limiting** - Prevent abuse with configurable limits  
✅ **Task Management** - Full CRUD with ownership validation  
✅ **Database Migrations** - Alembic for schema versioning  
✅ **Comprehensive Tests** - 20+ unit and integration tests  
✅ **Docker Ready** - production-ready containerization  

## Project Structure

```
app/
├── models/       # Database models
├── routers/      # API endpoints
├── schemas/      # Request/response validation
├── services/     # Business logic
├── utils/        # JWT, password, rate limiter
├── main.py       # FastAPI app
├── config.py     # Configuration
├── database.py   # DB setup
└── dependencies.py # Auth & injection
```

## Core Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/refresh` - Refresh access token
- `POST /oauth/{provider}/callback` - OAuth callback

### Tasks
- `POST /tasks` - Create task
- `GET /tasks` - List user's tasks
- `GET /tasks/{id}` - Get task details
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Users
- `GET /users/me` - Current user profile
- `PUT /users/me` - Update profile
- `GET /users` - List users (admin)
- `GET /users/{id}` - Get user (admin)

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret

# App
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_auth.py -v

# Check coverage
pytest --cov=app tests/
```

Currently: **20 passing tests** covering authentication, OAuth, users, and tasks.

## Database

The application uses PostgreSQL with SQLAlchemy ORM and Alembic migrations.

**Models:**
- `User` - User accounts with email/password & OAuth
- `Task` - User tasks with ownership
- `OAuthAccount` - OAuth provider accounts linked to users

**Migrations:**
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Check current state
alembic current
```

## Security

- Passwords hashed with BCrypt
- JWT tokens with expiration
- Rate limiting on sensitive endpoints
- CORS configured for specific origins
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic

## Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Format code
black app/ tests/

# Run linter
pylint app/

# Type checking
mypy app/
```

## Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Documentation

Full API documentation with comprehensive examples is available in [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## Error Handling

The API uses standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Server Error

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/x`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push branch (`git push origin feature/x`)
5. Open Pull Request

## Roadmap

- WebSocket support for real-time updates
- Email verification
- Two-factor authentication (2FA)
- Team collaboration
- Task categories and tags
- Advanced filtering and search
- GraphQL endpoint
- API rate limit tiers

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Status**: ✅ Production Ready  
**Tests**: 20+ Unit & Integration Tests  
**Coverage**: Authentication, OAuth, Users, Tasks

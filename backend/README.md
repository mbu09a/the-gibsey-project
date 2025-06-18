# Gibsey Mycelial Network - Backend API

FastAPI backend for the AI-powered narrative OS, designed to evolve from a simple story reader to a full vector-driven, event-native narrative platform.

## 🏗️ Current State (Phase 1 Complete!)

**What's Implemented:**
- ✅ FastAPI project structure with Docker support
- ✅ Core API endpoints for StoryPage, Prompt, User/Session operations
- ✅ WebSocket endpoints for real-time updates
- ✅ **Cassandra + Stargate database with full schema**
- ✅ **Automatic data migration from frontend JSON**
- ✅ **Database abstraction (mock for dev, Cassandra for production)**
- ✅ CORS setup for frontend communication
- ✅ Mock streaming AI responses for development

**What's Coming Next:**
- 🔄 Supabase authentication (Phase 1, Step 3)
- 🔄 Vector embedding pipeline (Phase 2)
- 🔄 Real streaming LLM integration (Phase 2)
- 🔄 Kafka event backbone (Phase 3)
- 🔄 3D visualization & cluster integration (Phase 4)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Run with Docker (Recommended)
```bash
cd backend

# For development with mock database (faster startup)
DATABASE_URL=mock://localhost docker-compose up --build api redis

# For production with Cassandra (full setup)
docker-compose up --build
```

**Note**: Full Cassandra setup takes 2-3 minutes to initialize. The `db-init` service will set up the schema and migrate your data automatically.

### Run Locally
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Available Endpoints

### Core API Endpoints
- **GET** `/` - API information
- **GET** `/health` - Health check
- **GET** `/api/v1/stats` - Database and connection statistics

### Story Pages
- **GET** `/api/v1/pages/` - List pages with pagination and filtering
- **GET** `/api/v1/pages/{page_id}` - Get specific page
- **POST** `/api/v1/pages/` - Create new page
- **PUT** `/api/v1/pages/{page_id}` - Update page
- **GET** `/api/v1/pages/symbol/{symbol_id}` - Get pages by character
- **GET** `/api/v1/pages/{page_id}/children` - Get child pages

### Prompts
- **GET** `/api/v1/prompts/` - List available prompts
- **GET** `/api/v1/prompts/{prompt_id}` - Get specific prompt
- **POST** `/api/v1/prompts/` - Create new prompt
- **GET** `/api/v1/prompts/page/{page_id}` - Get context-aware prompts for page

### Users & Sessions
- **POST** `/api/v1/users/` - Create user
- **GET** `/api/v1/users/{user_id}` - Get user
- **GET** `/api/v1/users/username/{username}` - Get user by username
- **POST** `/api/v1/users/sessions` - Create session
- **GET** `/api/v1/users/sessions/{session_id}` - Get session
- **PUT** `/api/v1/users/sessions/{session_id}` - Update session
- **POST** `/api/v1/users/sessions/guest` - Create guest session

### Real-Time Communication
- **WebSocket** `/ws/{session_id}` - Real-time updates and streaming

## 🔌 WebSocket API

Connect to `ws://localhost:8000/ws/{session_id}` to receive real-time updates.

### Supported Message Types

**Client → Server:**
```json
{
  "type": "ai_chat_request",
  "data": {
    "prompt": "Tell me about consciousness",
    "character_id": "london-fox"
  }
}
```

**Server → Client:**
```json
{
  "type": "ai_response_stream",
  "data": {
    "response_id": "uuid",
    "token": "I must analyze this through...",
    "is_complete": false
  }
}
```

## 🧪 Testing

### API Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### WebSocket Test Page
- **Test Interface**: http://localhost:8000/test

### Example API Calls
```bash
# Get all pages
curl http://localhost:8000/api/v1/pages/

# Get pages for London Fox
curl http://localhost:8000/api/v1/pages/symbol/london-fox

# Create a guest session
curl -X POST http://localhost:8000/api/v1/users/sessions/guest

# Get API stats
curl http://localhost:8000/api/v1/stats
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── models.py          # Pydantic models (StoryPage, User, etc.)
│   ├── database.py        # Database abstraction (currently mock)
│   ├── websocket.py       # WebSocket connection management
│   └── api/
│       ├── __init__.py
│       ├── pages.py       # StoryPage endpoints
│       ├── prompts.py     # Prompt endpoints
│       └── users.py       # User/Session endpoints
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Development setup (fast startup, in-memory data)
ENVIRONMENT=development
DATABASE_URL=mock://localhost
REDIS_URL=redis://localhost:6379

# Production setup (persistent data, full features)
DATABASE_URL=cassandra://cassandra:9042
CASSANDRA_HOSTS=cassandra
CASSANDRA_KEYSPACE=gibsey_network
STARGATE_URL=http://stargate:8082

# TODO: Add when implementing
SUPABASE_URL=your_supabase_url
OPENAI_API_KEY=your_openai_key
```

## 🚧 Development Notes

### Database Options

**Mock Database** (`DATABASE_URL=mock://localhost`):
- ✅ Fast startup, in-memory storage
- ✅ Loads data from `../src/assets/texts.json`
- ⚠️ Data lost on restart
- 🎯 Perfect for development and testing

**Cassandra Database** (`DATABASE_URL=cassandra://cassandra:9042`):
- ✅ Production-ready, persistent storage
- ✅ Vector embeddings support (ready for Phase 2)
- ✅ Automatic schema setup and data migration
- ✅ Scalable, PRD-compliant architecture
- ⏱️ Takes 2-3 minutes to initialize

### WebSocket Features (Stubbed)
- Connection management ✅
- Mock streaming AI responses ✅
- Real-time vault updates ✅
- Ready for real AI integration

### Migration Path
1. **Phase 1**: Complete FastAPI foundation
2. **Phase 2**: Add Cassandra + real authentication
3. **Phase 3**: Vector embeddings + AI integration
4. **Phase 4**: Kafka events + full PRD features

## 🎯 Next Steps

1. **Test the API**: Use the test page and Swagger docs
2. **Frontend Integration**: Update React app to use live API
3. **Database Migration**: Replace mock with Cassandra
4. **Authentication**: Add Supabase integration
5. **AI Integration**: Connect real streaming LLMs

## 🐛 Troubleshooting

### Docker Issues
```bash
# Rebuild containers
docker-compose down && docker-compose up --build

# Check logs
docker-compose logs api
```

### Connection Issues
- Ensure ports 8000 and 6379 are available
- Check CORS settings if frontend can't connect
- Verify WebSocket URL format

### Development Setup
```bash
# Install dependencies locally
pip install -r requirements.txt

# Run tests (when added)
pytest

# Format code
black . && isort .
```

---

**Ready to build the future of narrative AI!** 🚀

Check the API docs at http://localhost:8000/api/docs once running.
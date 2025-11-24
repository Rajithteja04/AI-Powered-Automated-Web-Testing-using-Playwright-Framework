# Adhoc Testing Agent Architecture

## System Overview

The Adhoc Testing Agent is a comprehensive web-based platform that converts natural language test requirements into executable Playwright test scripts using AI-powered agents orchestrated through LangGraph.

## Core Architecture

### Multi-Tier Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Flask App     │    │   External APIs │
│                 │    │                 │    │                 │
│ • User Interface│◄──►│ • Routes        │◄──►│ • Google Gemini │
│ • Forms         │    │ • Templates     │    │ • Playwright    │
│ • Real-time UI  │    │ • Authentication│    │ • Redis Cache   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LangGraph     │    │   AI Agents     │    │   Database      │
│   Workflow      │    │                 │    │                 │
│ • State Machine │◄──►│ • Script Gen    │◄──►│ • User Data     │
│ • Flow Control  │    │ • Executor      │    │ • Test History  │
│ • Error Handling│    │ • Debugger      │    │ • Sessions      │
└─────────────────┘    │ • Stats Agg     │    └─────────────────┘
                       └─────────────────┘
```

## Component Architecture

### 1. Web Layer (Flask Application)

#### Application Structure
```
app.py (Main Application)
├── Configuration Management (config.py)
├── Database Models (models.py)
├── Form Definitions (forms.py)
├── Route Handlers (routes.py)
├── Authentication (auth.py)
├── Admin Interface (admin.py)
└── Error Handlers
```

#### Key Components

**Flask Application (`app.py`)**
- Central application factory
- Blueprint registration
- Middleware configuration
- Database initialization
- Logging setup

**Configuration (`config.py`)**
- Environment-based configuration
- Security settings (CSRF, secrets)
- Database connections
- External service integrations
- Caching and rate limiting

**Routes (`routes.py`)**
- RESTful endpoint definitions
- Request/response handling
- Authentication decorators
- Rate limiting integration
- Background task execution

### 2. AI Agent Layer (LangGraph Orchestration)

#### LangGraph Workflow Architecture

```
TestGenerationState
├── requirement: str
├── browser: str
├── playwright_script: str
├── execution_result: str
├── analysis: str
├── test_stats: dict
└── test_stats_report: str

Workflow Nodes:
├── script_generator → generate_playwright_script()
├── executor → execute_script()
├── debugger → debug_script()
├── stats_aggregator → aggregate_stats()
└── done → Final state
```

#### Agent Components

**Script Generator Agent**
- Uses Google Gemini 2.5 Flash
- Converts natural language to Playwright code
- Embeds test statistics collection
- Browser-specific script generation

**Code Generator Agent**
- Analyzes existing project structure from ZIP uploads
- Generates complete Flask/Django/FastAPI application code
- Creates routes, templates, CSS, JS, models, and forms
- Provides integration instructions with line numbers
- Generates comprehensive test scripts for new features

**Script Executor Agent**
- Executes generated Playwright scripts
- Parses JSON statistics output
- Handles timeouts and errors
- Manages browser lifecycle

**Script Debugger Agent**
- Analyzes execution failures
- Generates corrected scripts
- Provides detailed error analysis
- Iterative debugging support

**Statistics Aggregator Agent**
- Processes raw test metrics
- Formats readable reports
- Calculates performance indicators
- Generates comprehensive summaries

### 3. Data Layer

#### Database Schema

**User Model**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL
);
```

**Script History Model**
```sql
CREATE TABLE script_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    requirement TEXT NOT NULL,
    script TEXT NOT NULL,
    result TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

#### Data Flow Patterns

**Test Execution Flow**
1. User submits requirement
2. Script generation (cached if available)
3. Script execution with browser
4. Statistics collection and parsing
5. Result storage in database
6. UI update with results

**Authentication Flow**
1. User credentials validation
2. Session creation
3. Role-based access control
4. Permission checking per route

### 4. External Integrations

#### Google AI Integration
```python
# LangChain integration pattern
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

chain = prompt | llm
result = chain.invoke({"requirement": requirement})
```

#### Playwright Integration
```python
# Browser automation pattern
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # Test execution logic
    browser.close()
```

#### Caching Integration
```python
# Redis caching pattern
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL')
})

@cache.memoize(timeout=3600)
def generate_script(requirement, browser):
    # Expensive operation
    return result
```

## Security Architecture

### Authentication & Authorization

**Flask-Login Integration**
- Session-based authentication
- User role management
- Login/logout handling
- Protected route decorators

**Role-Based Access Control**
```python
@routes.route('/generate')
@login_required
@limiter.limit("10 per minute")
def generate():
    if current_user.role != 'developer':
        flash('Access denied. Developers only.', 'danger')
        return redirect(url_for('main.home'))
```

### Security Measures

**Input Validation**
- WTForms validation
- Regex pattern matching
- Length constraints
- CSRF protection

**Rate Limiting**
- Flask-Limiter integration
- Per-user limits
- Redis-backed storage
- Configurable thresholds

**Data Protection**
- Password hashing (Werkzeug)
- Environment variable secrets
- Secure session handling
- SQL injection prevention

## Performance Architecture

### Caching Strategy

**Multi-Level Caching**
- LLM Response Cache (1 hour)
- Statistics Cache (30 minutes)
- Template Fragment Cache
- Database Query Cache

**Cache Invalidation**
- Time-based expiration
- Manual invalidation on updates
- Cache warming strategies

### Asynchronous Processing

**Threading Pattern**
```python
def run_graph():
    graph = build_graph()
    return graph.invoke(state)

with ThreadPoolExecutor() as executor:
    future = executor.submit(run_graph)
    state = future.result(timeout=300)
```

**Background Tasks**
- Long-running test execution
- Email notifications (future)
- Report generation (future)

### Database Optimization

**Connection Management**
- SQLAlchemy connection pooling
- Query optimization
- Index utilization
- Connection recycling

**Query Patterns**
- Eager loading relationships
- Selective field loading
- Pagination implementation
- Search optimization

## Scalability Architecture

### Horizontal Scaling

**Stateless Application**
- No server-side sessions
- External session storage (Redis)
- Database-backed state
- Load balancer friendly

**Microservices Ready**
- Modular agent architecture
- API-first design
- Container-ready deployment
- Service mesh compatible

### Vertical Scaling

**Resource Optimization**
- Memory-efficient processing
- CPU-bound task management
- I/O optimization
- Browser instance pooling

## Monitoring & Observability

### Logging Architecture

**Structured Logging**
```python
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Log Levels**
- DEBUG: Development details
- INFO: General operations
- WARNING: Potential issues
- ERROR: Application errors
- CRITICAL: System failures

### Health Checks

**Application Health**
- Database connectivity
- External API availability
- Cache health
- Background job status

**System Metrics**
- Response times
- Error rates
- Resource utilization
- Test execution statistics

## Deployment Architecture

### Container Architecture

**Docker Multi-Stage Build**
```dockerfile
# Build stage
FROM python:3.11-slim as builder
# Dependencies installation

# Runtime stage
FROM python:3.11-slim as runtime
# Application runtime
```

**Container Orchestration**
- Kubernetes deployment manifests
- Service definitions
- ConfigMap and Secret management
- Horizontal Pod Autoscaling

### Infrastructure Architecture

**Production Stack**
```
Load Balancer (nginx)
    ↓
Application Servers (gunicorn)
    ↓
Database (PostgreSQL)
Cache (Redis)
    ↓
External APIs (Google AI)
```

**Development Stack**
```
Local Flask Server
    ↓
SQLite Database
File-based Cache
    ↓
External APIs
```

## Error Handling Architecture

### Exception Hierarchy

**Application Errors**
- ValidationError: Input validation failures
- AuthenticationError: Auth failures
- AuthorizationError: Permission failures
- ExecutionError: Test execution failures
- ExternalAPIError: Third-party API failures

**Error Recovery**
- Graceful degradation
- Retry mechanisms
- Fallback strategies
- User-friendly error messages

### Error Propagation

**LangGraph Error Handling**
```python
try:
    state = graph.invoke(initial_state)
except Exception as e:
    logger.error(f"Graph execution failed: {e}")
    # Error recovery logic
```

**Flask Error Handlers**
```python
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 error: {str(error)}')
    db.session.rollback()
    return render_template('500.html'), 500
```

## Testing Architecture

### Test Categories

**Unit Tests**
- Individual function testing
- Mock external dependencies
- Agent logic validation

**Integration Tests**
- API endpoint testing
- Database operations
- External service integration

**End-to-End Tests**
- Full workflow testing
- Browser automation verification
- User journey validation

### Test Infrastructure

**Testing Stack**
- pytest framework
- Playwright test runner
- Mock external APIs
- Test database isolation

## Future Architecture Considerations

### Microservices Evolution

**Service Decomposition**
- Script generation service
- Execution service
- Analytics service
- User management service

**API Gateway**
- Request routing
- Authentication aggregation
- Rate limiting centralization
- Response transformation

### Advanced Features

**Real-time Updates**
- WebSocket integration
- Live execution monitoring
- Progress notifications
- Collaborative testing

**Advanced Analytics**
- Test performance dashboards
- Historical trend analysis
- Predictive failure detection
- Automated test optimization

**Integration APIs**
- CI/CD pipeline integration
- Test management tool sync
- Notification systems
- Custom reporting APIs

This architecture provides a solid foundation for the Adhoc Testing Agent while maintaining flexibility for future enhancements and scaling requirements.

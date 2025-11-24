# Adhoc Testing Agent

A comprehensive web-based platform for generating and executing end-to-end test automation scripts using natural language requirements. Built with Flask, LangGraph, and Playwright.

## 🚀 Features

### Core Functionality
- **Natural Language Test Generation**: Convert plain English requirements into executable Playwright test scripts
- **Code Generation**: Generate complete Flask/Django/FastAPI application code (routes, templates, CSS, JS, models, forms) from natural language requirements with project analysis
- **Multi-Agent Architecture**: LangGraph-powered workflow with script generation, execution, debugging, statistics aggregation, and code generation
- **Dynamic Test Statistics**: Real-time collection of execution metrics, assertions, performance data, and accessibility scores
- **Cross-Browser Testing**: Support for Chrome/Chromium, Firefox, and Safari/WebKit browsers
- **User Authentication**: Role-based access control (Developer, QA, Admin)
- **Test History Management**: Save, search, and rerun previous test executions

### Security & Performance
- **Rate Limiting**: API protection with configurable request limits
- **Input Validation**: Comprehensive form validation with CSRF protection
- **Threading**: Non-blocking execution with 5-minute timeouts
- **Caching**: Intelligent caching for improved performance
- **Error Handling**: Robust error management and user feedback

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python Flask with SQLAlchemy
- **Frontend**: Bootstrap 5 with Jinja2 templates
- **AI/ML**: Google Gemini 2.5 Flash via LangChain
- **Automation**: Playwright for browser automation
- **Workflow**: LangGraph for multi-agent orchestration
- **Database**: SQLite (development) / PostgreSQL (production)
- **Caching**: Flask-Caching with Redis support

### Project Structure
```
adhoc-testing-agent/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── routes.py             # Flask routes and views
├── graph.py              # LangGraph workflow definition
├── auth.py               # Authentication utilities
├── admin.py              # Admin interface
├── agents/               # AI agent implementations
│   ├── __init__.py
│   ├── playwright_script_generator.py
│   ├── script_executor.py
│   ├── script_debugger.py
│   ├── stats_aggregator.py
│   └── code_generator.py
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── generate.html
│   ├── generate_code.html
│   ├── history.html
│   ├── users.html
│   ├── edit_user.html
│   └── 404.html
├── static/               # Static assets (CSS, JS, images)
├── utils/                # Utility functions
│   └── zip_handler.py
├── instance/             # Instance-specific data
├── requirements.txt      # Python dependencies
├── test.py              # Test suite
└── README.md            # This file
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for Playwright browsers)
- Google AI API key
- Redis (optional, for caching)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd adhoc-testing-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Set environment variables**
   ```bash
   export GOOGLE_API_KEY="your-google-api-key"
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## 🚀 Usage

### Starting the Application
```bash
flask run
```

Access the application at `http://localhost:5000`

### Creating Tests

1. **Login** with developer credentials
2. **Navigate** to Generate Test page
3. **Select Browser** (Chrome, Firefox, or Safari)
4. **Choose** a predefined requirement or write custom requirement
5. **Submit** to generate and execute the test
6. **View Results** including script, execution status, and statistics

### Generating Code

1. **Login** with developer credentials
2. **Navigate** to Generate Code page
3. **Select Browser** (Chrome, Firefox, or Safari)
4. **Write** your code generation requirement in natural language
5. **Upload** your existing project as a ZIP file for analysis
6. **Submit** to generate complete application code
7. **View Results** including generated routes, templates, CSS, JS, and integration instructions

### User Roles

- **Developer**: Can generate and execute tests, generate code
- **QA Engineer**: Can view test history and rerun tests
- **Admin**: Full access including user management

## 🔧 Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your-api-key
FLASK_APP=app.py
FLASK_ENV=development

# Optional
REDIS_URL=redis://localhost:6379
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key
```

### Rate Limiting
- Generate endpoint: 10 requests per minute
- Rerun endpoint: 5 requests per minute

### Caching
- Script generation: 1 hour cache
- Statistics aggregation: 30 minutes cache

## 📊 Test Statistics

The system collects comprehensive metrics for each test execution:

- **Execution Time**: Total test duration
- **Assertions**: Pass/fail counts with error details
- **Step Coverage**: Completed test steps
- **Performance**: Page load times and action durations
- **Accessibility**: Violation counts
- **Locator Stability**: Retry/fallback metrics

## 🧪 Testing

### Running Tests
```bash
python test.py
```

### Manual Testing Scenarios
1. **Basic Login Test**: SauceDemo login verification
2. **E-commerce Flow**: Search → Add to Cart → Checkout
3. **Error Handling**: Invalid credentials, network failures
4. **Cross-Browser**: Same test across different browsers

## 🔒 Security

- **CSRF Protection**: Enabled on all forms
- **Input Sanitization**: Regex validation for requirements
- **Rate Limiting**: Prevents abuse
- **Session Management**: Secure Flask sessions
- **Password Hashing**: Werkzeug security

## 📈 Performance

- **Concurrent Execution**: Threaded processing
- **Caching**: Intelligent result caching
- **Timeout Management**: 5-minute execution limits
- **Resource Optimization**: Efficient browser management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📝 API Documentation

### Endpoints

#### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `POST /logout` - User logout

#### Testing
- `GET/POST /generate` - Generate and execute tests
- `GET/POST /generate-code` - Generate application code with project analysis
- `GET/POST /history` - View test history
- `POST /rerun/<id>` - Rerun specific test
- `GET /download/<id>` - Download test script

#### Administration
- `GET /admin/users` - User management
- `POST /admin/users/<id>/edit` - Edit user
- `POST /admin/users/<id>/delete` - Delete user

## 🐛 Troubleshooting

### Common Issues

1. **Browser Launch Failures**
   ```bash
   playwright install --force
   ```

2. **API Key Errors**
   - Verify GOOGLE_API_KEY is set
   - Check API quota and billing

3. **Database Errors**
   ```bash
   flask db migrate
   flask db upgrade
   ```

4. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **Playwright** - Browser automation
- **LangChain** - AI orchestration
- **Bootstrap** - UI framework
- **Google Gemini** - AI model

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Version**: 1.0.0
**Last Updated**: 2025
**Maintainer**: Development Team

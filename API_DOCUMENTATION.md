# Adhoc Testing Agent API Documentation

## Overview

The Adhoc Testing Agent provides RESTful API endpoints for test automation management. All endpoints require authentication and follow role-based access control.

## Authentication

### Login
**POST** `/login`

Authenticate user and establish session.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "user",
    "role": "developer"
  }
}
```

### Logout
**POST** `/logout`

End user session.

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Test Management

### Generate Test
**POST** `/generate`

Generate and execute a test script from natural language requirements.

**Required Role:** Developer

**Rate Limit:** 10 requests per minute

**Request Body:**
```json
{
  "browser": "chromium|firefox|webkit",
  "requirement": "Test login functionality on SauceDemo website"
}
```

**Response:**
```json
{
  "success": true,
  "script": "Generated Playwright script...",
  "execution_result": "[PASS] Execution succeeded.",
  "analysis": "Analysis of any issues...",
  "test_stats_report": "📊 Test Statistics Report:\n- Execution Time: 5.96s\n..."
}
```

### Get Test History
**GET** `/history`

Retrieve paginated list of test executions.

**Required Role:** Developer, QA

**Query Parameters:**
- `search` (optional): Search term for filtering
- `page` (optional): Page number (default: 1)

**Response:**
```json
{
  "success": true,
  "scripts": [
    {
      "id": 1,
      "requirement": "Login test",
      "script": "Playwright script...",
      "result": "Execution result...",
      "timestamp": "2024-01-01T12:00:00Z",
      "user": {
        "username": "developer1"
      }
    }
  ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

### Rerun Test
**POST** `/rerun/{script_id}`

Re-execute a previously run test.

**Required Role:** Developer, QA

**Rate Limit:** 5 requests per minute

**Response:**
```json
{
  "success": true,
  "message": "Script re-run completed successfully"
}
```

### Download Test Script
**GET** `/download/{script_id}`

Download the generated test script as a Python file.

**Required Role:** Developer, QA

**Response:** Python file download

### Generate Code
**POST** `/generate-code`

Generate Flask application code (routes, templates, CSS, JS) and tests from natural language requirements with project zip upload for code analysis.

**Required Role:** Developer

**Rate Limit:** 5 requests per minute

**Request Body (Form Data):**
```
browser: chromium|firefox|webkit
requirement: "Add a user profile page with edit functionality"
project_zip: [zip file upload]
```

**Response:**
```json
{
  "success": true,
  "generated_code": {
    "routes_code": "Complete routes.py additions...",
    "template_code": {
      "profile.html": "Complete HTML template..."
    },
    "css_code": {
      "profile.css": "Complete CSS styles..."
    },
    "js_code": {
      "profile.js": "Complete JavaScript..."
    },
    "models_code": "Any new model additions...",
    "forms_code": "Any new form additions..."
  },
  "integration_instructions": "Detailed integration guide with line numbers...",
  "playwright_script": "Generated test script...",
  "execution_result": "[PASS] Test execution succeeded.",
  "test_stats_report": "📊 Test Statistics Report..."
}
```

### Generate Test
**POST** `/generate`

Generate and execute a test script from natural language requirements.

**Required Role:** Developer

**Rate Limit:** 10 requests per minute

**Request Body:**
```json
{
  "browser": "chromium|firefox|webkit",
  "requirement": "Test login functionality on SauceDemo website"
}
```

**Response:**
```json
{
  "success": true,
  "script": "Generated Playwright script...",
  "execution_result": "[PASS] Execution succeeded.",
  "analysis": "Analysis of any issues...",
  "test_stats_report": "📊 Test Statistics Report:\n- Execution Time: 5.96s\n..."
}
```

## Administration

### List Users
**GET** `/admin/users`

Get all users (admin only).

**Required Role:** Admin

**Response:**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  ]
}
```

### Create User
**POST** `/admin/users`

Create a new user.

**Required Role:** Admin

**Request Body:**
```json
{
  "username": "newuser",
  "password": "password123",
  "role": "developer"
}
```

### Update User
**PUT** `/admin/users/{user_id}`

Update user information.

**Required Role:** Admin

### Delete User
**DELETE** `/admin/users/{user_id}`

Delete a user.

**Required Role:** Admin

## Error Responses

All endpoints return standardized error responses:

```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

### Common Error Codes
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid input data
- `RATE_LIMITED`: Too many requests
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

## Rate Limiting

- **Generate endpoint**: 10 requests per minute per user
- **Rerun endpoint**: 5 requests per minute per user
- **Other endpoints**: No specific limits

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

## Data Models

### User
```json
{
  "id": "integer",
  "username": "string",
  "role": "developer|qa|admin"
}
```

### Script History
```json
{
  "id": "integer",
  "user_id": "integer",
  "requirement": "string",
  "script": "string",
  "result": "string",
  "timestamp": "datetime"
}
```

### Test Statistics
```json
{
  "execution_time": "float",
  "assertions_passed": "integer",
  "assertions_failed": "integer",
  "total_assertions": "integer",
  "step_coverage": ["string"],
  "performance": {
    "page_loads": ["float"],
    "action_times": ["float"]
  },
  "accessibility_violations": "integer",
  "locator_retries": "integer",
  "errors": ["string"]
}
```

## WebSocket Support

Real-time updates for long-running test executions are available via WebSocket:

**Endpoint:** `ws://localhost:5000/test-updates`

**Messages:**
```json
{
  "type": "progress",
  "data": {
    "stage": "generating|executing|analyzing",
    "progress": 75
  }
}
```

## SDK Examples

### Python Client
```python
import requests

class TestingAgentClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password):
        response = self.session.post(f"{self.base_url}/login",
                                   json={"username": username, "password": password})
        return response.json()

    def generate_test(self, requirement, browser="chromium"):
        response = self.session.post(f"{self.base_url}/generate",
                                   json={"requirement": requirement, "browser": browser})
        return response.json()
```

### JavaScript Client
```javascript
class TestingAgentClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }

    async login(username, password) {
        const response = await fetch(`${this.baseUrl}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        return response.json();
    }

    async generateTest(requirement, browser = 'chromium') {
        const response = await fetch(`${this.baseUrl}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ requirement, browser })
        });
        return response.json();
    }
}
```

## Versioning

API versioning follows semantic versioning (MAJOR.MINOR.PATCH).

Current version: **1.0.0**

## Changelog

### Version 1.0.0
- Initial API release
- Basic CRUD operations for tests and users
- Authentication and authorization
- Rate limiting and caching
- Cross-browser test execution

## Support

For API support:
- Check this documentation
- Review error messages
- Contact development team

---

**API Version**: 1.0.0
**Last Updated**: 2025

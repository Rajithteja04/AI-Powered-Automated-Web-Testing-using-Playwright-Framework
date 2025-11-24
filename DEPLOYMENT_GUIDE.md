# Adhoc Testing Agent Deployment Guide

## Overview

This guide covers deployment options for the Adhoc Testing Agent in various environments including development, staging, and production.

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Node.js**: 16+ (for Playwright)
- **Memory**: Minimum 2GB RAM, recommended 4GB+
- **Storage**: 1GB free space
- **Network**: Internet access for API calls

### External Services
- **Google AI API**: For script generation
- **Redis** (optional): For caching and rate limiting
- **PostgreSQL** (optional): For production database

## Quick Start Deployment

### Local Development

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd adhoc-testing-agent
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Database setup**
   ```bash
   export FLASK_APP=app.py
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Run application**
   ```bash
   flask run
   ```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Playwright
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium firefox webkit

# Copy application
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Docker Compose (Full Stack)
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/testing_agent
      - REDIS_URL=redis://redis:6379
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./instance:/app/instance

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=testing_agent
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

#### Build and Run
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build single container
docker build -t testing-agent .
docker run -p 5000:5000 -e GOOGLE_API_KEY=your-key testing-agent
```

## Production Deployment

### Heroku Deployment

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your-api-key
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Database setup**
   ```bash
   heroku run flask db upgrade
   ```

5. **Install Playwright browsers**
   ```bash
   heroku run playwright install
   ```

### AWS EC2 Deployment

1. **Launch EC2 instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium or higher
   - Storage: 20GB+ SSD

2. **Security group configuration**
   - SSH (22)
   - HTTP (80)
   - HTTPS (443)
   - Custom TCP (5000) for Flask

3. **Server setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv -y

   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Clone repository
   git clone <repository-url>
   cd adhoc-testing-agent

   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn

   # Install Playwright
   playwright install --with-deps

   # Setup environment
   cp .env.example .env
   # Edit .env with production values
   ```

4. **Nginx configuration**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **Systemd service**
   ```ini
   [Unit]
   Description=Adhoc Testing Agent
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/adhoc-testing-agent
   Environment="PATH=/home/ubuntu/adhoc-testing-agent/venv/bin"
   ExecStart=/home/ubuntu/adhoc-testing-agent/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Kubernetes Deployment

#### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testing-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: testing-agent
  template:
    metadata:
      labels:
        app: testing-agent
    spec:
      containers:
      - name: testing-agent
        image: your-registry/testing-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: testing-agent-secrets
              key: database-url
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: testing-agent-secrets
              key: google-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

#### Service YAML
```yaml
apiVersion: v1
kind: Service
metadata:
  name: testing-agent-service
spec:
  selector:
    app: testing-agent
  ports:
    - port: 80
      targetPort: 5000
  type: LoadBalancer
```

#### Ingress YAML
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: testing-agent-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: testing-agent-service
            port:
              number: 80
```

## Environment Configuration

### Environment Variables

#### Required
```bash
GOOGLE_API_KEY=your-google-api-key
SECRET_KEY=your-flask-secret-key
```

#### Optional
```bash
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379
LOG_LEVEL=INFO
WTF_CSRF_SECRET_KEY=csrf-secret-key
```

### Configuration Files

#### .env.example
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=change-this-in-production
WTF_CSRF_SECRET_KEY=change-this-too

# Database
DATABASE_URL=sqlite:///app.db

# External Services
GOOGLE_API_KEY=your-api-key-here
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```

## Monitoring and Maintenance

### Health Checks

The application provides health check endpoints:

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

### Logging

Configure logging for production:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### Backup Strategy

#### Database Backup
```bash
# PostgreSQL
pg_dump -U username -h host database > backup.sql

# SQLite
cp instance/app.db instance/app.db.backup
```

#### Automated Backups
```bash
# Cron job for daily backups
0 2 * * * pg_dump -U username database > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Performance Optimization

1. **Gunicorn configuration**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 --timeout 300 app:app
   ```

2. **Database optimization**
   - Use connection pooling
   - Add database indexes
   - Enable query logging

3. **Caching strategy**
   - Cache LLM responses
   - Cache static assets
   - Use Redis for session storage

## Troubleshooting

### Common Issues

#### Playwright Browser Issues
```bash
# Reinstall browsers
playwright install --force

# Check browser installation
playwright install-deps
```

#### Memory Issues
```bash
# Monitor memory usage
htop

# Adjust Gunicorn workers
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

#### Database Connection Issues
```bash
# Test database connection
python -c "from app import db; db.engine.execute('SELECT 1')"
```

#### API Key Issues
```bash
# Verify API key
curl -H "Authorization: Bearer $GOOGLE_API_KEY" \
     "https://generativelanguage.googleapis.com/v1beta/models"
```

### Logs and Debugging

#### Application Logs
```bash
# View recent logs
tail -f app.log

# Search for errors
grep "ERROR" app.log
```

#### System Logs
```bash
# System logs
journalctl -u testing-agent

# Nginx logs
tail -f /var/log/nginx/error.log
```

## Security Considerations

### Production Security
- Use HTTPS with valid SSL certificates
- Implement proper firewall rules
- Regular security updates
- Monitor for vulnerabilities
- Use environment variables for secrets
- Implement rate limiting
- Enable CSRF protection

### Backup Security
- Encrypt backups
- Store backups securely
- Test backup restoration
- Implement backup rotation

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use Redis for session sharing
- Implement database read replicas

### Vertical Scaling
- Increase instance size for CPU/memory intensive tasks
- Optimize database queries
- Implement caching layers

## Support

For deployment issues:
1. Check application logs
2. Verify environment configuration
3. Test API endpoints manually
4. Review system resources
5. Contact development team

---

**Deployment Version**: 1.0.0
**Last Updated**: 2025

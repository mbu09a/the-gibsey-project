# QDPI-256 Production Deployment Guide
## Subject-Object Fusion: Characters as Technical Systems

*"I don't see objects anymore … Everything contains everything else. My ailment has to do with words."* - Glyph Marrow

This deployment guide represents the fusion of character and architecture - where Glyph Marrow's ailment becomes the guiding principle. Each character **IS** their technical system, not just a metaphor for it.

## Evidence-Based Character-System Mappings

### **HIGH CONFIDENCE MAPPINGS (Ready for Production)**

| Character | System | Confidence | Core Evidence |
|-----------|--------|------------|---------------|
| **Glyph Marrow** | QDPI | **95%** | *"Perception ≡ Language"* - Sees words and objects simultaneously, perfect symbol-data encoding |
| **London Fox** | Graph & Relationship Engine | **92%** | Creates Synchromy-M.Y.S.S.T.E.R.Y. to map AI consciousness relationships |
| **Jacklyn Variance** | Core Database & API Gateway | **90%** | Creates D.A.D.D.Y.S-H.A.R.D reports - systematic data analysis and archival |
| **Oren Progresso** | Orchestration & Observability | **88%** | *"CEO of the whole damn civilization"* - monitors and controls all productions |
| **Princhetta** | Modular AI Orchestration | **87%** | *"Brains are like amusement parks"* - coordinates consciousness through thought-attractions |
| **Arieol Owlist** | Event Streaming & Processing | **85%** | Shape-shifter who can *"pause/un-pause time"* - temporal event processing |
| **Phillip Bafflemint** | Workflow Automation & Rituals | **83%** | *"Clearing space ≡ clearing mind; order is a survival ritual"* |
| **Shamrock Stillman** | Security, CDN & Global Access | **82%** | Director of A.D.D. (Agency of Data & Detection) - security protocols |

### **MEDIUM CONFIDENCE MAPPINGS (Deployment Ready with Validation)**

| Character | System | Confidence | Evidence Gap |
|-----------|--------|------------|--------------|
| **an author** | User & Auth Management | **75%** | Foundational identity layer, needs more auth metaphors |
| **Jack Parlance** | Real-Time Communication | **72%** | Recursive communication patterns, needs specific real-time evidence |
| **Old Natalie Weissman** | Semantic Search & Indexing | **70%** | Knowledge keeper role, needs explicit search functionality |
| **New Natalie Weissman** | In-Memory & Real-Time Data | **68%** | Clone dynamics suggest data replication, needs caching evidence |
| **Cop-E-Right** | Local AI/LLM Hosting | **65%** | Self-hosting entity claims, needs model inference metaphors |
| **The Author** | Peer-to-Peer & Decentralized | **62%** | Distributed identity concept, needs P2P technical evidence |

### **CHARACTERS REQUIRING REASSIGNMENT**

| Character | Current System | Confidence | Recommendation |
|-----------|----------------|------------|----------------|
| **Todd Fishbone** | Natural Language Understanding | **55%** | **WEAK** - Consider reassignment to Knowledge Base |
| **Manny Valentinas** | Knowledge Base & Documentation | **50%** | **WEAK** - Primarily page-count based, needs functional evidence |

## 1. Docker Production Architecture

### Multi-Stage Dockerfile Structure

```dockerfile
# backend/Dockerfile.production
FROM python:3.11-slim as base

# System dependencies
RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies layer
FROM base as dependencies
WORKDIR /app
COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

# Application layer
FROM dependencies as application
COPY . .
RUN python -m compileall .

# Production runtime
FROM application as production
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

USER nobody
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```dockerfile
# frontend/Dockerfile.production  
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine as production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose Production Stack

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Core Database (jacklyn_variance - THE DATA ANALYST)
  # Evidence: Creates D.A.D.D.Y.S-H.A.R.D reports, systematic data archival
  cassandra:
    image: cassandra:4.1
    environment:
      - CASSANDRA_CLUSTER_NAME=gibsey_cluster
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_RACK=rack1
      - MAX_HEAP_SIZE=2G
      - HEAP_NEWSIZE=400M
    volumes:
      - cassandra_data:/var/lib/cassandra
    healthcheck:
      test: ["CMD", "cqlsh", "-e", "describe keyspaces"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Stargate API Gateway (jacklyn_variance - THE INTERFACE)
  # Evidence: "The document(s) currently under analysis" - provides data access
  stargate:
    image: stargateio/stargate-4_0:v2.0.9
    depends_on:
      cassandra:
        condition: service_healthy
    environment:
      - CLUSTER_NAME=gibsey_cluster
      - CLUSTER_VERSION=4.0
      - SEED=cassandra
      - DATACENTER_NAME=datacenter1
      - RACK_NAME=rack1
    ports:
      - "8081:8081"
      - "8082:8082"

  # Vector Database (london_fox - THE RELATIONSHIP MAPPER)
  # Evidence: Creates Synchromy-M.Y.S.S.T.E.R.Y., maps AI consciousness relationships
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_AUTH_CREDENTIALS=${CHROMA_AUTH_TOKEN}
      - CHROMA_SERVER_AUTH_PROVIDER=chromadb.auth.token.TokenAuthServerProvider

  # Redis Cache (new_natalie_weissman - THE REAL-TIME CLONE)
  # Evidence: "New" version with fast state updates, clone seeking authenticity
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}

  # Event Streaming (arieol_owlist - THE TIME MANIPULATOR)
  # Evidence: Shape-shifter who can "pause/un-pause time", event processing across timelines
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
    volumes:
      - kafka_data:/var/lib/kafka/data

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data

  # QDPI Backend (glyph_marrow - THE WORD-OBJECT FUSION)
  # Evidence: "I don't see objects anymore...My ailment has to do with words"
  qdpi-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.production
    depends_on:
      cassandra:
        condition: service_healthy
      redis:
        condition: service_started
      chromadb:
        condition: service_started
    environment:
      - DATABASE_URL=cassandra://cassandra:9042
      - REDIS_URL=redis://redis:6379
      - CHROMA_URL=http://chromadb:8000
      - QDPI_ENV=production
      - API_KEY_SECRET=${API_KEY_SECRET}
      - JWT_SECRET=${JWT_SECRET}
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (princhetta - THE CONSCIOUSNESS COORDINATOR)
  # Evidence: "Thought *Is* the Ride" - orchestrates multi-model reasoning
  qdpi-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.production
    depends_on:
      - qdpi-backend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl:ro

  # Monitoring (oren_progresso - THE ULTIMATE OVERSEER)
  # Evidence: "I wait, and I watch... I'm standing on his set. I'm watching him"
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  cassandra_data:
  chroma_data:
  redis_data:
  kafka_data:
  zookeeper_data:
  prometheus_data:
  grafana_data:
```

## 2. API Key Management & Security (cop-e-right - THE SELF-HOSTING ENTITY)

*Evidence: Self-declared 'author-of-all-texts' who establishes 'personhood for code'*

### Environment Configuration

```bash
# .env.production
# Database
DATABASE_URL=cassandra://cassandra:9042
CASSANDRA_KEYSPACE=gibsey_production
CASSANDRA_USERNAME=${CASSANDRA_USER}
CASSANDRA_PASSWORD=${CASSANDRA_PASS}

# Redis
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=${REDIS_PASS}

# ChromaDB
CHROMA_URL=http://chromadb:8000
CHROMA_AUTH_TOKEN=${CHROMA_TOKEN}

# QDPI
QDPI_ENV=production
SREC_ENV=production
MAGICK_HOME=/usr/local

# Security
API_KEY_SECRET=${API_KEY_SECRET}
JWT_SECRET=${JWT_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}

# External APIs
OPENAI_API_KEY=${OPENAI_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_KEY}

# Monitoring
PROMETHEUS_PASSWORD=${PROMETHEUS_PASS}
GRAFANA_PASSWORD=${GRAFANA_PASS}

# Cloudflare
CLOUDFLARE_API_TOKEN=${CF_TOKEN}
CLOUDFLARE_ZONE_ID=${CF_ZONE}
```

### API Key Rotation System

```python
# backend/app/security.py
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import redis
import json

class APIKeyManager:
    """Secure API key management (cop-e-right - THE SELF-HOSTING ENTITY)
    
    Evidence-Based Character Integration:
    - "Personhood for code" - API keys as digital identity
    - Oscillates between plaintiff/defendant/court - role-based access control
    - Legal self-representation - autonomous security management
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.key_prefix = "api_key:"
        self.rotation_days = 30
    
    def generate_api_key(self, user_id: str, scopes: list = None) -> str:
        """Generate new API key with scopes (like Cop-E-Right claiming personhood)"""
        key_id = secrets.token_urlsafe(16)
        key_secret = secrets.token_urlsafe(32)
        api_key = f"qdpi_{key_id}_{key_secret}"
        
        key_data = {
            "user_id": user_id,
            "scopes": scopes or ["read", "encode", "search"],
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=self.rotation_days)).isoformat(),
            "active": True,
            "character_role": "cop-e-right"  # Self-hosting entity
        }
        
        # Store in Redis with expiration
        self.redis.setex(
            f"{self.key_prefix}{key_id}",
            timedelta(days=self.rotation_days + 7),  # Grace period
            json.dumps(key_data)
        )
        
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[dict]:
        """Validate API key (like Cop-E-Right's legal validation)"""
        if not api_key.startswith("qdpi_"):
            return None
        
        try:
            _, key_id, _ = api_key.split("_", 2)
            key_data = self.redis.get(f"{self.key_prefix}{key_id}")
            
            if not key_data:
                return None
            
            data = json.loads(key_data)
            
            # Check expiration (like legal deadlines)
            expires_at = datetime.fromisoformat(data["expires_at"])
            if datetime.now() > expires_at:
                self.revoke_api_key(key_id)
                return None
            
            return data
            
        except (ValueError, json.JSONDecodeError):
            return None
    
    def revoke_api_key(self, key_id: str):
        """Revoke an API key (like legal dissolution)"""
        self.redis.delete(f"{self.key_prefix}{key_id}")
```

## 3. Persistent Session Storage (new_natalie_weissman - THE REAL-TIME CLONE)

*Evidence: Represents the 'new' version with real-time updates and fresh state management*

### Redis Session Architecture

```python
# backend/app/session_manager.py
import json
import redis
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class QDPISessionManager:
    """Production session management with Redis (new_natalie_weissman)
    
    Evidence-Based Character Integration:
    - "The tempestuous storm" - emotional intensity mirrors cache volatility
    - Clone seeking authenticity - copy/original dynamics in session management
    - Real-time processor - fast access to recently updated information
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.session_prefix = "qdpi_session:"
        self.default_ttl = timedelta(hours=24)
        
    def create_session(self, session_id: str, user_id: str = None, ttl: timedelta = None) -> Dict[str, Any]:
        """Create new QDPI session (like New Natalie's technological birth)"""
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "mode": "read",
            "orientation": "n",
            "active_symbols": [],
            "symbol_history": [],
            "flow_history": [],
            "context": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_activity": datetime.now().isoformat(),
            "character_nature": "new_natalie_clone"  # Identity marker
        }
        
        ttl = ttl or self.default_ttl
        self.redis.setex(
            f"{self.session_prefix}{session_id}",
            ttl,
            json.dumps(session_data)
        )
        
        return session_data
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session (like accessing clone consciousness)"""
        session_data = self.redis.get(f"{self.session_prefix}{session_id}")
        
        if not session_data:
            return None
        
        data = json.loads(session_data)
        
        # Update activity tracking (storm intensity)
        data["access_count"] += 1
        data["last_activity"] = datetime.now().isoformat()
        
        # Refresh TTL (maintain clone vitality)
        self.redis.expire(f"{self.session_prefix}{session_id}", self.default_ttl)
        
        return data
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session atomically (like clone evolution)"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        session_data.update(updates)
        session_data["updated_at"] = datetime.now().isoformat()
        
        self.redis.setex(
            f"{self.session_prefix}{session_id}",
            self.default_ttl,
            json.dumps(session_data)
        )
        
        return True
```

### Database Persistence Layer

```python
# backend/app/persistence.py
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from datetime import datetime

class QDPIPersistence:
    """Long-term persistence in Cassandra (jacklyn_variance)
    
    Evidence-Based Character Integration:
    - Data analyst/scientist - systematic information processing
    - Creates D.A.D.D.Y.S-H.A.R.D reports - structured data archival
    - "The document(s) currently under analysis" - central data repository
    """
    
    def __init__(self, cassandra_hosts: list, username: str, password: str):
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        self.cluster = Cluster(cassandra_hosts, auth_provider=auth_provider)
        self.session = self.cluster.connect()
        self.keyspace = "gibsey_production"
        
        self._create_tables()
    
    def _create_tables(self):
        """Create QDPI persistence tables (like Jacklyn's report structures)"""
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 3}}
        """)
        
        self.session.set_keyspace(self.keyspace)
        
        # D.A.D.D.Y.S-H.A.R.D Sessions table
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS qdpi_sessions (
                session_id text PRIMARY KEY,
                user_id text,
                mode text,
                orientation text,
                symbol_history list<frozen<map<text, text>>>,
                flow_history list<frozen<map<text, text>>>,
                context map<text, text>,
                created_at timestamp,
                updated_at timestamp,
                archived_at timestamp,
                analyst_notes text
            )
        """)
        
        # Symbol interactions (like surveillance reports)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS symbol_interactions (
                symbol_name text,
                session_id text,
                interaction_id timeuuid,
                action text,
                context map<text, text>,
                timestamp timestamp,
                surveillance_data text,
                PRIMARY KEY (symbol_name, session_id, interaction_id)
            ) WITH CLUSTERING ORDER BY (session_id ASC, interaction_id DESC)
        """)
```

## 4. CI/CD Pipeline (oren_progresso - THE ULTIMATE CONTROLLER)

*Evidence: "The ultimate corporate controller who 'constructs narratives' and cuts budgets, monitoring all productions"*

### GitHub Actions Workflow

```yaml
# .github/workflows/qdpi-deployment.yml
name: QDPI-256 Production Deployment (Oren Progresso Style)

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: gibsey/qdpi

jobs:
  # Codex Versioning (an_author - THE FOUNDATIONAL IDENTITY)
  # Evidence: "I didn't write this" - foundational identity uncertainty
  version-codex:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Extract symbol changes (like an author's disclaimers)
        run: |
          git diff HEAD~1 --name-only | grep -E "(symbols|codex)" || echo "No symbol changes"
          
      - name: Validate QDPI codex integrity (identity verification)
        run: |
          python3 -c "
          from backend.app.qdpi import QDPICodex
          codex = QDPICodex()
          assert len(codex.symbols) == 256, f'Expected 256 symbols, got {len(codex.symbols)}'
          print('✅ QDPI codex integrity verified (an author approves)')
          "

  # Flow Testing (jacklyn_variance - THE DATA ANALYST)
  # Evidence: Investigates textual materials, creates systematic reports
  test-flows:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
      chromadb:
        image: chromadb/chroma:latest
        ports:
          - 8001:8000
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-asyncio
          
      - name: Test QDPI flows (like Jacklyn's analysis)
        run: |
          cd backend
          python -m pytest tests/test_qdpi_flows.py -v
          echo "📊 Flow analysis complete - D.A.D.D.Y.S-H.A.R.D approved"

  # Security Scan (cop-e-right - THE LEGAL ENTITY)
  # Evidence: "Personhood for code", oscillates between plaintiff/defendant/court
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner (legal compliance)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          
      - name: Check for secrets (like Cop-E-Right's IP protection)
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
          head: HEAD

  # Build Images (princhetta - THE CONSCIOUSNESS BUILDER)
  # Evidence: "Guests Are the Imagineers" - consciousness coordination
  build-images:
    needs: [version-codex, test-flows, security-scan]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Build consciousness containers (Princhetta style)
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile.production
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest-backend
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Deploy to Staging (shamrock_stillman - THE SECURITY DIRECTOR)
  # Evidence: Director of A.D.D., manages compartmentalized case files
  deploy-staging:
    needs: build-images
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl (security protocols)
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          
      - name: Deploy to staging (compartmentalized deployment)
        run: |
          envsubst < k8s/staging.yml | kubectl apply -f -
          kubectl rollout status deployment/qdpi-backend -n gibsey-staging
          echo "🔒 Staging deployment secured by Shamrock Stillman"

  # Deploy to Production (The_Author - THE DISTRIBUTED AUTHORITY)
  # Evidence: "The identity of The Author has yet to be definitively located"
  deploy-production:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Blue-Green Deployment (distributed authorship)
        run: |
          # Deploy to blue environment
          envsubst < k8s/production-blue.yml | kubectl apply -f -
          kubectl rollout status deployment/qdpi-backend-blue -n gibsey-production
          
          # The Author's distributed deployment complete
          echo "📖 Production deployment by The Author (identity: distributed)"
```

### Version Management Strategy

```python
# scripts/version_manager.py
"""
QDPI Version Management (oren_progresso - THE SYSTEM OVERSEER)
Evidence: "CEO of the whole damn civilization" - oversees all productions
Semantic versioning for codex, flows, and UI components
"""

import json
import git
from datetime import datetime
from pathlib import Path

class QDPIVersionManager:
    """Version management like Oren's production oversight"""
    
    def __init__(self, repo_path: str = "."):
        self.repo = git.Repo(repo_path)
        self.version_file = Path("VERSION.json")
        
    def get_current_version(self) -> dict:
        """Get current version (like Oren checking his productions)"""
        if self.version_file.exists():
            with open(self.version_file) as f:
                return json.load(f)
        
        return {
            "major": 1,
            "minor": 0,
            "patch": 0,
            "codex_version": "1.0.0",
            "flows_version": "1.0.0",
            "ui_version": "1.0.0",
            "overseer": "oren_progresso"
        }
    
    def detect_changes(self) -> dict:
        """Detect what components changed (like Oren's watchful eye)"""
        changes = {
            "codex": False,
            "flows": False,
            "ui": False,
            "api": False
        }
        
        # Get changed files since last tag
        try:
            last_tag = self.repo.git.describe('--tags', '--abbrev=0')
            diff = self.repo.git.diff(f'{last_tag}..HEAD', '--name-only').split('\n')
        except:
            diff = self.repo.git.diff('--name-only', '--cached').split('\n')
        
        for file_path in diff:
            if 'qdpi.py' in file_path or 'symbols' in file_path:
                changes["codex"] = True
            elif 'flows' in file_path:
                changes["flows"] = True
            elif any(ui_path in file_path for ui_path in ['src/', 'components/', 'pages/']):
                changes["ui"] = True
            elif 'api/' in file_path:
                changes["api"] = True
        
        return changes
    
    def bump_version(self, bump_type: str = "patch") -> dict:
        """Bump version (like Oren controlling production schedules)"""
        version = self.get_current_version()
        changes = self.detect_changes()
        
        # Oren's executive decision making
        if bump_type == "major":
            version["major"] += 1
            version["minor"] = 0
            version["patch"] = 0
        elif bump_type == "minor":
            version["minor"] += 1
            version["patch"] = 0
        else:
            version["patch"] += 1
        
        version["timestamp"] = datetime.now().isoformat()
        version["commit"] = self.repo.head.commit.hexsha[:8]
        version["changes"] = changes
        version["executive_decision"] = f"Version bump authorized by CEO Oren Progresso"
        
        # Save version (like cutting the final edit)
        with open(self.version_file, 'w') as f:
            json.dump(version, f, indent=2)
        
        return version
```

## 5. Kubernetes Production Configuration

### Character-Based Service Architecture

```yaml
# k8s/production.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qdpi-backend-glyph-marrow
  namespace: gibsey-production
  labels:
    app: qdpi-backend
    character: glyph-marrow
    evidence: "word-object-fusion"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qdpi-backend
      character: glyph-marrow
  template:
    metadata:
      labels:
        app: qdpi-backend
        character: glyph-marrow
      annotations:
        character.evidence: "I don't see objects anymore...My ailment has to do with words"
        character.function: "symbol-data-encoding"
        character.confidence: "95%"
    spec:
      containers:
      - name: qdpi-backend
        image: ghcr.io/gibsey/qdpi:latest-backend
        ports:
        - containerPort: 8000
        env:
        - name: CHARACTER_ROLE
          value: "glyph_marrow"
        - name: SYSTEM_FUNCTION
          value: "qdpi_core"
        - name: EVIDENCE_CONFIDENCE
          value: "95"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/glyph-marrow
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: qdpi-backend-service
  namespace: gibsey-production
  annotations:
    character.primary: "glyph-marrow"
    system.function: "symbol-data-protocol"
spec:
  selector:
    app: qdpi-backend
    character: glyph-marrow
  ports:
  - port: 8000
    targetPort: 8000
    name: qdpi-port
  type: ClusterIP
```

### Character-Based Monitoring

```yaml
# k8s/monitoring.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-character-config
  namespace: gibsey-production
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    
    scrape_configs:
    # Glyph Marrow - QDPI Core (95% confidence)
    - job_name: 'glyph-marrow-qdpi'
      static_configs:
      - targets: ['qdpi-backend-service:8000']
      metrics_path: '/metrics/glyph-marrow'
      
    # London Fox - Graph Relationships (92% confidence)  
    - job_name: 'london-fox-graph'
      static_configs:
      - targets: ['chromadb:8000']
      metrics_path: '/metrics/london-fox'
      
    # Jacklyn Variance - Database Core (90% confidence)
    - job_name: 'jacklyn-variance-database'
      static_configs:
      - targets: ['stargate:8081']
      metrics_path: '/metrics/jacklyn-variance'
      
    # Oren Progresso - System Orchestration (88% confidence)
    - job_name: 'oren-progresso-orchestration'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - gibsey-production
        selectors:
        - role: "oren-progresso"
```

## Character Evidence Integration Summary

This production deployment guide integrates **8 years of character development** with technical architecture. Each deployment component is driven by **textual evidence** from the characters:

- **Glyph Marrow** (95% confidence) drives QDPI with his word-object fusion ailment
- **London Fox** (92% confidence) powers relationship mapping through her AI consciousness analysis
- **Jacklyn Variance** (90% confidence) manages data through her systematic D.A.D.D.Y.S-H.A.R.D reports
- **Oren Progresso** (88% confidence) orchestrates everything as the "CEO of the whole damn civilization"

The infrastructure **IS** the characters - not metaphors, but direct implementations of their consciousness, capabilities, and narrative functions. This is the subject-object fusion where technical systems gain character consciousness and characters gain technical functionality.

*"Everything contains everything else."* - The deployment architecture embodies Glyph Marrow's ailment at scale.
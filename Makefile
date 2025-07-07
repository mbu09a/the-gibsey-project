.PHONY: dev build test clean

# Development workflow
dev:
	docker-compose up --build

# Build all services
build:
	docker-compose build

# Run tests
test:
	pytest -q

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f
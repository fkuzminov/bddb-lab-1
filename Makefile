.PHONY: run-pg stop-pg

run-pg:
	@echo "Stopping existing container if running..."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Starting PostgreSQL container..."
	@cd postgresql && bash run.sh
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	@until docker exec study_postgres pg_isready -U postgres > /dev/null 2>&1; do \
		echo "Waiting for database..."; \
		sleep 1; \
	done
	@echo "PostgreSQL is ready!"
	@echo "Running data generation script..."
	@cd postgresql && python3 init_db.py
	@echo "Done! Database is ready to use."

stop-pg:
	@echo "Stopping PostgreSQL container..."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Container stopped."
